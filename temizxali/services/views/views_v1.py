from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.db.models import Prefetch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string

from services.models import *
from services.forms import OrderForm
from services.forms import ReviewForm
from services.utils import ServiceQuery


__all__ = [
    'HomePageView',
    'AboutPageView',
    'OrderPageView',
    'CalculatorPageView',
    'ServiceDetailPage',
    'ReviewCreateView',
    'ProjectsPaginationView',
    'ProjectsPageView',
    'TestimonialPageView',
]


class HomePageView(View):
    template_name = 'index.html'

    def get(self, request):
        from services.utils.homepage_queries import HomePageQueries
        
        lang = translation.get_language()
        data = HomePageQueries.get_all_homepage_data(lang)
        
        return render(request, self.template_name, data)


class AboutPageView(View):
    template_name = 'about.html'

    def get(self, request):
        from services.utils.about_queries import AboutPageQueries
        
        lang = translation.get_language()
        data = AboutPageQueries.get_all_about_data(lang)
        
        return render(request, self.template_name, data)


class ServiceDetailPage(View):
    template_name = 'service_detail_page.html'
    
    def get(self, request, service_slug):
        from services.utils.service_detail_queries import ServiceDetailQueries
        
        lang = translation.get_language()
        data = ServiceDetailQueries.get_service_detail_data(lang, service_slug)
        
        return render(request, self.template_name, data)


class OrderPageView(View):
    template_name = 'contact.html'
    
    def get(self, request):
        form = OrderForm()
        services = ServiceQuery.load_services()
        current_language = translation.get_language()
        contact = Contact.objects.first()
        calculator_background_image = Image.objects.filter(
            is_calculator_page_background_image=True
        ).first()
        return render(request, self.template_name, {
            'form': form,
            'services': services,
            'current_language': current_language,
            'view_type': 'order',
            'contact': contact,
            'calculator_background_image': calculator_background_image,
        })
    
    def post(self, request):
        form = OrderForm(request.POST)
        services = ServiceQuery.load_services()
        current_language = translation.get_language()
        contact = Contact.objects.first()
        calculator_background_image = Image.objects.filter(
            is_calculator_page_background_image=True
        ).first()
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
                    'calculator_background_image': calculator_background_image,
                })
        else:
            messages.error(request, _('Zəhmət olmasa formu düzgün doldurun'))
            return render(request, self.template_name, {
                'form': form,
                'services': services,
                'current_language': current_language,
                'view_type': 'order',
                'contact': contact,
                'calculator_background_image': calculator_background_image,
            })
    

class CalculatorPageView(View):
    template_name = 'calculator.html'
    
    def get(self, request):
        services = ServiceQuery.load_services()
        current_language = translation.get_language()
        contact = Contact.objects.first()
        calculator_background_image = Image.objects.filter(
            is_calculator_page_background_image=True
        ).first()
        return render(request, self.template_name, {
            'services': services,
            'current_language': current_language,
            'contact': contact,
            'calculator_background_image': calculator_background_image,
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
        review_background_image = Image.objects.filter(
            is_review_page_background_image=True
        ).first()
        return render(request, self.template_name, {
            'form': form,
            'services': services,
            'contact': contact,
            'review_background_image': review_background_image,
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
        review_background_image = Image.objects.filter(
            is_review_page_background_image=True
        ).first()

        if form.is_valid():
            form.save()
            messages.success(request, _('Rəyiniz uğurla göndərildi ✅'))
        else:
            messages.error(request, _('Melumatlari duzgun daxil edin'))

        return render(request, self.template_name, {
            'form': form,
            'services': services,
            'contact': contact,
            'review_background_image': review_background_image,
        })
    

class ProjectsPaginationView(View):
    def get(self, request):
        languages = translation.get_language()
        special_projects = SpecialProject.objects.filter(
            is_active=True,
            translations__languages=languages
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=SpecialProjectTranslation.objects.filter(languages=languages)),
            'images'
        ).order_by('-created_at')
        
        paginator = Paginator(special_projects, 6)
        page = request.GET.get('page', 1)
        try:
            projects_page = paginator.page(page)
        except PageNotAnInteger:
            projects_page = paginator.page(1)
        except EmptyPage:
            projects_page = paginator.page(paginator.num_pages)
        
        projects_html = render_to_string('projects_partial.html', {
            'special_projects': projects_page,
        }, request=request)
        
        pagination_html = render_to_string('pagination_partial.html', {
            'special_projects': projects_page,
        }, request=request)
        
        return JsonResponse({
            'projects_html': projects_html,
            'pagination_html': pagination_html,
            'current_page': projects_page.number,
            'total_pages': paginator.num_pages
        })


class ProjectsPageView(View):
    template_name = 'projects.html'
    
    def get(self, request):
        from services.utils.projects_queries import ProjectsPageQueries
        
        lang = translation.get_language()
        page = request.GET.get('page', 1)
        data = ProjectsPageQueries.get_all_projects_data(lang, page=int(page))
        
        return render(request, self.template_name, data)


class TestimonialPageView(View):
    template_name = 'testimonial.html'
    
    def get(self, request):
        languages = translation.get_language()
        reviews = Review.objects.filter(is_verified=True).prefetch_related(
            Prefetch('service__translations', queryset=ServiceTranslation.objects.filter(languages=languages))
        ).order_by('-created_at')
        services = Service.objects.filter(
            is_active=True,
            translations__languages=languages
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=ServiceTranslation.objects.filter(languages=languages))
        ).order_by('-created_at')
        contact = Contact.objects.first()
        testimonial_background_image = Image.objects.filter(
            is_testimonial_page_background_image=True
        ).first()
        
        return render(request, self.template_name, {
            'reviews': reviews,
            'services': services,
            'contact': contact,
            'current_language': languages,
            'testimonial_background_image': testimonial_background_image,
        })

