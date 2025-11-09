from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.db.models import Prefetch
from django.conf import settings
from django.urls import reverse
from decimal import Decimal
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.conf import settings

from services.models import *
from services.forms import OrderForm
from services.forms import ReviewForm
from services.utils import CalculatorService, CalculatorQuery


__all__ = [
    'HomePageView',
    'AboutPageView',
    'OrderPageView',
    'ServiceDetailPage',
    'ReviewCreateView',
    'ServiceCalculatorView'
]

@method_decorator(cache_page(settings.CACHE_TTL), name='dispatch')
class HomePageView(View):
    template_name = 'index.html'
    
    def get(self, request):
        languages = translation.get_language()
        background_images = Image.objects.filter(
            is_background_image=True
        ).order_by('-created_at')
        services = Service.objects.filter(
            is_active=True,
            translations__languages=languages
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=ServiceTranslation.objects.filter(languages=languages)),
            'images'
        ).order_by('-created_at')
        special_projects = SpecialProject.objects.filter(
            is_active=True,
            translations__languages=languages
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=SpecialProjectTranslation.objects.filter(languages=languages)),
            'images'
        ).order_by('-created_at')
        
        statistics = Statistic.objects.first()
        mottos = Motto.objects.filter(
            translations__languages=languages
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=MottoTranslation.objects.filter(languages=languages))
        ).order_by('-id')
        reviews = Review.objects.filter(is_verified=True).order_by('-created_at')
        contact = Contact.objects.first()

        mottos_with_bg = []
        background_images_list = list(background_images)
        if mottos.exists() and background_images_list:
            for index, motto in enumerate(mottos):
                bg_image = background_images_list[index % len(background_images_list)]
                mottos_with_bg.append({
                    'motto': motto,
                    'background_image': bg_image
                })
        elif mottos.exists():
            for motto in mottos:
                mottos_with_bg.append({
                    'motto': motto,
                    'background_image': None
                })

        return render(request, self.template_name, {
            'languages': languages,
            'background_images': background_images,
            'background_image': background_images.first() if background_images.exists() else None,
            'mottos_with_bg': mottos_with_bg,
            'services': services,
            'special_projects': special_projects,
            'statistics': statistics,
            'mottos': mottos,
            'reviews': reviews,
            'contact': contact
        })

@method_decorator(cache_page((settings.CACHE_TTL)), name='dispatch')
class AboutPageView(View):
    template_name = 'about_page.html'

    def get(self, request):
        languages = translation.get_language()
        about = About.objects.all().distinct().prefetch_related(
            Prefetch('translations', queryset=AboutTranslation.objects.filter(languages=languages))
        )
        statistics = Statistic.objects.all()

        return render(request, self.template_name, {
            'about': about,
            'statistics': statistics,
            'active_lang': languages,
            })

@method_decorator(cache_page((settings.CACHE_TTL)), name='dispatch')
class ServiceDetailPage(View):
    template_name = 'service_detail_page.html'
    def get(self, request, service_slug):
        languages = translation.get_language()
        translation_obj = get_object_or_404(
            ServiceTranslation,
            slug=service_slug
        )
        service = translation_obj.service
        current_lang_translation = service.translations.filter(
            languages=languages
        ).first()
        display_translation = current_lang_translation if current_lang_translation else translation_obj
        service = Service.objects.filter(
            id=service.id
        ).prefetch_related(
            Prefetch('translations', queryset=ServiceTranslation.objects.filter(
                languages=languages
            )),
            'images',
            Prefetch('variants', queryset=ServiceVariant.objects.all().prefetch_related(
                Prefetch('translations', queryset=ServiceVariantTranslation.objects.filter(languages=languages))
            ))
        ).first()
        sale_price = None
        sale_vip_price = None
        sale_premium_price = None
        
        if service.sale:
            sale_percent = Decimal(str(service.sale)) / Decimal('100')
            if service.price:
                sale_price = Decimal(str(service.price)) * (Decimal('1') - sale_percent)
            if service.vip_price:
                sale_vip_price = Decimal(str(service.vip_price)) * (Decimal('1') - sale_percent)
            if service.premium_price:
                sale_premium_price = Decimal(str(service.premium_price)) * (Decimal('1') - sale_percent)

        return render(request, self.template_name, {
            'languages': languages,
            'service': service,
            'translation': display_translation,
            'sale_price': sale_price,
            'sale_vip_price': sale_vip_price,
            'sale_premium_price': sale_premium_price,
            })


class OrderPageView(View):
    template_name = 'contact.html'
    
    def get(self, request):
        form = OrderForm()
        services = CalculatorQuery.load_services()
        current_language = translation.get_language()
        contact = Contact.objects.first()
        return render(request, self.template_name, {
            'form': form,
            'services': services,
            'current_language': current_language,
            'view_type': 'order',
            'contact': contact,
        })
    
    def post(self, request):
        form = OrderForm(request.POST)
        services = CalculatorQuery.load_services()
        current_language = translation.get_language()
        contact = Contact.objects.first()
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _('Sifarişiniz uğurla göndərildi'))
                return redirect('order-page')
            except Exception as e:
                messages.error(request, _('Xəta baş verdi: %s') % str(e))
                return render(request, self.template_name, {
                    'form': form,
                    'services': services,
                    'current_language': current_language,
                    'view_type': 'order',
                    'contact': contact,
                })
        else:
            messages.error(request, _('Zəhmət olmasa formu düzgün doldurun'))
            return render(request, self.template_name, {
                'form': form,
                'services': services,
                'current_language': current_language,
                'view_type': 'order',
                'contact': contact,
            })
    


class ReviewCreateView(View):
    template_name = 'comment_add.html'

    def get(self, request):
        languages = translation.get_language()
        form = ReviewForm()
        services = Service.objects.filter(
            is_active=True,
            translations__languages=languages
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=ServiceTranslation.objects.filter(languages=languages))
        ).order_by('-created_at')
        contact = Contact.objects.first()
        return render(request, self.template_name, {
            'form': form,
            'services': services,
            'contact': contact
        })

    def post(self, request):
        languages = translation.get_language()
        form = ReviewForm(request.POST)
        services = Service.objects.filter(
            is_active=True,
            translations__languages=languages
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=ServiceTranslation.objects.filter(languages=languages))
        ).order_by('-created_at')
        contact = Contact.objects.first()

        if form.is_valid():
            form.save()
            messages.success(request, _('Rəyiniz uğurla göndərildi ✅'))
            return redirect('review-success')
        else:
            messages.error(request, _('Melumatlari duzgun daxil edin'))

        return render(request, self.template_name, {
            'form': form,
            'services': services,
            'contact': contact
        })
    


class ServiceCalculatorView(View):
    """
    Handles display and processing of the service price calculator.
    """
    template_name = 'contact.html'

    def get(self, request):
        """
        Handle GET requests to render the calculator page.

        - Activates language based on the session or query.
        - Loads available services.
        - Retrieves any stored calculation results from the session.
        """
        self._language_switch(request)
        services = CalculatorQuery.load_services()
        result = []
        total_price = Decimal('0.00')

        if 'calculator_result' in request.session:
            result = request.session.pop('calculator_result')
            total_price = Decimal(request.session.pop('calculator_total'))

        form = OrderForm()
        contact = Contact.objects.first()
        return render(request, self.template_name, {
            'services': services,
            'result': result,
            'total_price': total_price,
            'form': form,
            'current_language': translation.get_language(),
            'view_type': 'calculator',
            'contact': contact,
        })

    def post(self, request):
        """
        Handle POST requests to calculate selected services' total price.

        - Reads selected service IDs from the request.
        - Applies each service to the calculator service.
        - Stores the calculation result in the session.
        """
        lang = translation.get_language()
        service_ids = request.POST.getlist('service_id')

        if not service_ids:
            messages.warning(request, _('Heç bir servis seçilməyib.'))
            return redirect(self._redirect_with_lang())

        calc = CalculatorService(lang)

        for sid in service_ids:
            services = CalculatorQuery.load_services()
            try:
                service = services.get(id=sid, is_active=True)
                calc.apply_item(request, service)
            except:
                pass

        request.session['calculator_result'] = calc.result
        request.session['calculator_total'] = str(calc.total_price)
        return redirect(self._redirect_with_lang())

    def _redirect_with_lang(self):
        """
        Build redirect URL that preserves the current language parameter.

        Returns:
            str: URL with language code if not default.
        """
        lang = translation.get_language()
        url = reverse('service_calculator')
        if lang != settings.LANGUAGE_CODE:
            url += f'?lang={lang}'
        return url

    def _language_switch(self, request):
        """
        Handle language switching from query parameters.

        Activates the requested language and stores it in session if valid.
        """
        lang_param = request.GET.get('lang') or request.GET.get('language')
        if lang_param and lang_param in dict(settings.LANGUAGES):
            request.session['django_language'] = lang_param
            translation.activate(lang_param)
