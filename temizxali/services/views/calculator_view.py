from decimal import Decimal
from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _
from django.conf import settings

from services.models import (
    Service,
    ServiceTranslation,
    ServiceVariantTranslation,
)


def service_calculator(request):
    # GET parametri ilə dil seçimi
    lang_param = request.GET.get('lang') or request.GET.get('language')
    if lang_param and lang_param in dict(settings.LANGUAGES):
        request.session['django_language'] = lang_param
        translation.activate(lang_param)
    
    lang = translation.get_language()
    result = []
    total_price = Decimal("0.00")
    services = (
        Service.objects.filter(
            is_active=True,
            translations__languages=lang,
        )
        .distinct()
        .prefetch_related(
            Prefetch(
                "translations",
                queryset=ServiceTranslation.objects.filter(languages=lang),
            ),
            Prefetch(
                "variants__translations",
                queryset=ServiceVariantTranslation.objects.filter(
                    languages=lang
                ),
            ),
        )
    )

    if request.method == "POST":
        service_ids = request.POST.getlist("service_id")

        if not service_ids:
            messages.warning(request, _("Heç bir servis seçilməyib."))
            redirect_url = reverse("service_calculator")
            if lang != settings.LANGUAGE_CODE:
                redirect_url += f"?lang={lang}"
            return redirect(redirect_url)

        for service_id in service_ids:
            if not service_id:
                continue

            try:
                service = (
                    Service.objects.prefetch_related(
                        Prefetch(
                            "translations",
                            queryset=ServiceTranslation.objects.filter(
                                languages=lang
                            ),
                        ),
                        Prefetch(
                            "variants__translations",
                            queryset=ServiceVariantTranslation.objects.filter(
                                languages=lang
                            ),
                        ),
                    )
                    .get(id=service_id, is_active=True)
                )
            except Service.DoesNotExist:
                messages.error(
                    request, _("Servis tapılmadı: ID %(service_id)s") % {"service_id": service_id}
                )
                continue

            service_name = (
                service.translations.first().name
                if service.translations.exists()
                else f"Servis{service.id}"
            )

            variant_ids = request.POST.getlist(f"variant_{service_id}")
            selected_variants = []
            for vid in variant_ids:
                if vid:
                    try:
                        variant = service.variants.get(id=vid)
                        selected_variants.append(variant)
                    except Exception:
                        pass

            if not selected_variants:
                selected_variants = [None]

            for variant in selected_variants:
                value_key = (
                    f"value_{service_id}"
                    + (f"_{variant.id}" if variant else "")
                )
                value_input = request.POST.get(value_key, "").strip()

                if not value_input:
                    messages.warning(
                        request, _("%(service_name)s üçün dəyər daxil edilməyib.") % {"service_name": service_name}
                    )
                    continue

                try:
                    value = Decimal(value_input)
                    if value <= 0:
                        messages.warning(
                            request,
                            _("%(service_name)s üçün dəyər müsbət olmalıdır.") % {"service_name": service_name},
                        )
                        continue
                except (ValueError, Decimal.InvalidOperation):
                    messages.warning(
                        request, _("%(service_name)s üçün keçərsiz dəyər.") % {"service_name": service_name}
                    )
                    continue

                price_type_key = (
                    f"price_type_{service_id}"
                    + (f"_{variant.id}" if variant else "")
                )
                price_type = request.POST.get(price_type_key, "normal")

                if variant:
                    base_price = (
                        variant.vip_price
                        if price_type == "vip" and variant.vip_price
                        else variant.premium_price
                        if price_type == "premium" and variant.premium_price
                        else variant.price or Decimal("0.00")
                    )
                    variant_name = (
                        variant.translations.first().name
                        if variant.translations.exists()
                        else ""
                    )
                else:
                    base_price = (
                        service.vip_price
                        if price_type == "vip" and service.vip_price
                        else service.premium_price
                        if price_type == "premium" and service.premium_price
                        else service.price or Decimal("0.00")
                    )
                    variant_name = ""

                if service.is_kq:
                    unit = "kq"
                    calculated = base_price * value
                elif service.is_kv_metr:
                    unit = "m²"
                    calculated = base_price * value
                elif service.is_metr:
                    unit = "m"
                    calculated = base_price * value
                else:
                    unit = "ədəd"
                    calculated = base_price

                discount_percent = Decimal(str(service.sale or "0"))
                discount_amount = (calculated * discount_percent) / Decimal(
                    "100"
                )
                final_price = calculated - discount_amount

                total_price += final_price

                result.append(
                    {
                        "service": service,
                        "service_name": service_name,
                        "variant": variant,
                        "variant_name": variant_name,
                        "price_type": price_type,
                        "value": value,
                        "base_price": base_price,
                        "calculated_before_discount": calculated,
                        "discount_amount": discount_amount,
                        "discount_percent": discount_percent,
                        "final_price": final_price,
                        "unit": unit,
                    }
                )

        if result:
            request.session["calculator_result"] = [
                {
                    "service_id": r["service"].id,
                    "service_name": r["service_name"],
                    "variant_id": r["variant"].id if r["variant"] else None,
                    "variant_name": r["variant_name"],
                    "price_type": r["price_type"],
                    "value": str(r["value"]),
                    "base_price": str(r["base_price"]),
                    "calculated_before_discount": str(
                        r["calculated_before_discount"]
                    ),
                    "discount_amount": str(r["discount_amount"]),
                    "discount_percent": str(r["discount_percent"]),
                    "final_price": str(r["final_price"]),
                    "unit": r["unit"],
                }
                for r in result
            ]
            request.session["calculator_total"] = str(total_price)

        redirect_url = reverse("service_calculator")
        if lang != settings.LANGUAGE_CODE:
            redirect_url += f"?lang={lang}"
        return redirect(redirect_url)

    if "calculator_result" in request.session:
        data = request.session.pop("calculator_result", [])
        total_price = Decimal(
            request.session.pop("calculator_total", "0.00")
        )

        for item in data:
            try:
                service = (
                    Service.objects.prefetch_related(
                        Prefetch(
                            "translations",
                            queryset=ServiceTranslation.objects.filter(
                                languages=lang
                            ),
                        ),
                        Prefetch(
                            "variants__translations",
                            queryset=ServiceVariantTranslation.objects.filter(
                                languages=lang
                            ),
                        ),
                    )
                    .get(id=item["service_id"], is_active=True)
                )

                variant = None
                if item.get("variant_id"):
                    try:
                        variant = service.variants.get(
                            id=item["variant_id"]
                        )
                    except Exception:
                        pass

                result.append(
                    {
                        "service": service,
                        "service_name": item["service_name"],
                        "variant": variant,
                        "variant_name": item["variant_name"],
                        "price_type": item["price_type"],
                        "value": Decimal(item["value"]),
                        "base_price": Decimal(item["base_price"]),
                        "calculated_before_discount": Decimal(
                            item["calculated_before_discount"]
                        ),
                        "discount_amount": Decimal(item["discount_amount"]),
                        "discount_percent": Decimal(item["discount_percent"]),
                        "final_price": Decimal(item["final_price"]),
                        "unit": item["unit"],
                    }
                )
            except Exception:
                continue

    return render(
        request,
        "calculator.html",
        {
            "services": services,
            "result": result,
            "total_price": total_price,
            "current_language": lang,
        },
    )