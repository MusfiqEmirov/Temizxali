from decimal import Decimal
from django.contrib import messages
from django.utils.translation import gettext as _

class CalculatorService:
    """
    Service class for calculating total prices of selected services and variants.
    Handles dynamic price types, discounts, and unit-based calculations.
    """
    def __init__(self, lang):
        """
        Initialize the calculator with language and default totals.

        Args:
            lang (str): The current active language code.
        """
        self.lang = lang
        self.result = []
        self.total_price = Decimal('0.00')

    def apply_item(self, request, service):
        """
        Process a single service and add its calculation result.

        Args:
            request (HttpRequest): The current request object containing form data.
            service (Service): The service instance being calculated.

        Returns:
            None
        """
        return self._process(request, service)

    def _process(self, request, service):
        """
        Internal method to process the calculation logic for a service.

        - Retrieves variants and input values from POST data.
        - Applies base prices, price type (normal/premium/vip).
        - Calculates discounts and totals.
        - Appends calculation details to `self.result`.

        Args:
            request (HttpRequest): The request object containing POST data.
            service (Service): The service instance being processed.

        Returns:
            None
        """
        service_name = service.translations.first().name if service.translations.exists() else f'Servis{service.id}'
        variant_ids = request.POST.getlist(f'variant_{service.id}')
        selected_variants = []

        for vid in variant_ids:
            try:
                selected_variants.append(service.variants.get(id=vid))
            except:
                pass

        if not selected_variants:
            selected_variants = [None]

        for variant in selected_variants:
            value_key = f'value_{service.id}' + (f'_{variant.id}' if variant else '')
            price_key = f'price_type_{service.id}' + (f'_{variant.id}' if variant else '')
            value_input = request.POST.get(value_key, '').strip()
            price_type = request.POST.get(price_key, 'normal')

            if not value_input:
                messages.warning(request, _('%(service_name)s üçün dəyər daxil edilməyib.') % {'service_name': service_name})
                continue

            try:
                value = Decimal(value_input)
                if value <= 0:
                    messages.warning(request, _('%(service_name)s üçün dəyər müsbət olmalıdır.') % {'service_name': service_name})
                    continue
            except:
                messages.warning(request, _('%(service_name)s üçün keçərsiz dəyər.') % {'service_name': service_name})
                continue

            if variant:
                raw_price = (
                    variant.vip_price if price_type == 'vip' and variant.vip_price else
                    variant.premium_price if price_type == 'premium' and variant.premium_price else
                    variant.price
                )
                base_price = Decimal(str(raw_price)) if raw_price is not None else Decimal('0')
                variant_name = variant.translations.first().name if variant.translations.exists() else ''
            else:
                raw_price = (
                    service.vip_price if price_type == 'vip' and service.vip_price else
                    service.premium_price if price_type == 'premium' and service.premium_price else
                    service.price
                )
                base_price = Decimal(str(raw_price)) if raw_price is not None else Decimal('0')
                variant_name = ''

            # Calculate based on measure_type
            measure_type = service.measure_type
            if measure_type == 'kg':
                calculated = base_price * value
                unit = 'kq'
            elif measure_type == 'm2':
                calculated = base_price * value
                unit = 'm²'
            elif measure_type == 'm':
                calculated = base_price * value
                unit = 'm'
            elif measure_type == 'unit':
                calculated = base_price * value
                unit = 'ədəd'
            else:
                calculated = base_price
                unit = 'ədəd'

            # Get applicable SaleEvent discount based on min_quantity
            # SaleEvent service-ə bağlıdır və service-in measure_type-ı ilə uyğun olmalıdır
            discount_percent = Decimal('0')
            applicable_sale = None
            
            # Find active SaleEvent that matches service measure_type and min_quantity condition
            try:
                # Prefetch edilmiş sales-i istifadə et, yoxdursa query et
                if hasattr(service, '_prefetched_objects_cache') and 'sales' in service._prefetched_objects_cache:
                    sales_queryset = service._prefetched_objects_cache['sales']
                else:
                    sales_queryset = service.sales.filter(active=True)
                
                for sale_event in sales_queryset:
                    # Yalnız aktiv sale event-ləri nəzərə al
                    if not getattr(sale_event, 'active', False):
                        continue
                    # SaleEvent service-ə bağlıdır, ona görə də service-in measure_type-ı ilə uyğun olur
                    min_qty = Decimal(str(getattr(sale_event, 'min_quantity', 0)))
                    if value >= min_qty:
                        sale_percent = getattr(sale_event, 'sale', None)
                        if sale_percent and (not applicable_sale or sale_percent > getattr(applicable_sale, 'sale', 0)):
                            applicable_sale = sale_event
            except (AttributeError, Exception):
                # Əgər sales mövcud deyilsə və ya xəta baş verərsə, endirim yoxdur
                pass
            
            if applicable_sale:
                sale_percent = getattr(applicable_sale, 'sale', None)
                if sale_percent:
                    discount_percent = Decimal(str(sale_percent))
            
            discount_amount = (calculated * discount_percent) / Decimal('100')
            final_price = calculated - discount_amount

            self.total_price += final_price

            self.result.append({
                'service': service,
                'service_name': service_name,
                'variant': variant,
                'variant_name': variant_name,
                'price_type': price_type,
                'value': value,
                'base_price': base_price,
                'calculated_before_discount': calculated,
                'discount_amount': discount_amount,
                'discount_percent': discount_percent,
                'final_price': final_price,
                'unit': unit,
            })
