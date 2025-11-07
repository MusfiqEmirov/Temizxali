from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.db.models import Prefetch
from django.conf import settings
from django.urls import reverse
from decimal import Decimal

from services.models import *
from services.forms import OrderForm
from services.forms import ReviewForm
from services.utils.calculator import CalculatorService
from services.utils.query import CalculatorQuery


__all__ = [
    'HomePageView',
    'OrderCreateView',
    'OrderSuccessView',
    'ReviewCreateView',
    'ReviewSuccessView',
    'ServiceCalculatorView'
]


class HomePageView(View):
    template_name = 'home_page.html'
    def get(self, request):
        languages = translation.get_language()

        background_image = Image.objects.filter(
            image_name='home_page_background', 
            is_background_image=True
        ).first()
        services = Service.objects.filter(
            is_active=True,
            translations__languages = languages
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=ServiceTranslation.objects.filter(languages=languages)),
            'images'
        )
        special_projects = SpecialProject.objects.filter(
            is_active=True,
            translations__languages = languages
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=SpecialProjectTranslation.objects.filter(languages=languages)),
            'images'
        )
        statistics = Statistic.objects.all()
        reviews = Review.objects.filter(is_verified=True)

        return render(request, self.template_name, {
            'background_image': background_image,
            'services': services,
            'special_projects': special_projects,
            'statistics': statistics,
            'reviews': reviews
            })


class OrderCreateView(View):
    template_name = 'order_form.html'
    
    def get(self, request):
        form = OrderForm()
        current_language = translation.get_language()
        return render(request, self.template_name, {
            'form': form,
            'current_language': current_language,
        })
    
    def post(self, request):
        form = OrderForm(request.POST)
        current_language = translation.get_language()
        if form.is_valid():
            form.save()
            messages.success(request, _('Sifarişiniz uğurla göndərildi'))
            return redirect('order-success')
        else:
            messages.error(request, _('Zəhmət olmasa formu düzgün doldurun'))
            return render(request, self.template_name, {
                'form': form,
                'current_language': current_language,
            })
    


class OrderSuccessView(View):
    template_name = 'order_success.html'

    def get(self, request):
        '''Sifarişin uğurla göndərildiyi səhifə'''
        return render(request, self.template_name)
    

class ReviewCreateView(View):
    '''Rəy əlavə etmək üçün səhifə'''
    template_name = 'review_form.html'

    def get(self, request):
        '''Formu göstərir'''
        form = ReviewForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        '''Formu emal edir'''
        form = ReviewForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, _('Rəyiniz uğurla göndərildi ✅'))
            return redirect('review-success')
        else:
            messages.error(request, _('Melumatlari duzgun daxil edin'))

        return render(request, self.template_name, {'form': form})
    

class ReviewSuccessView(View):
    template_name = 'review_success.html'

    def get(self, request):
        return render(request, self.template_name)


class ServiceCalculatorView(View):
    """
    Handles display and processing of the service price calculator.
    """
    template_name = 'calculator.html'

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

        return render(request, self.template_name, {
            'services': services,
            'result': result,
            'total_price': total_price,
            'current_language': translation.get_language(),
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
