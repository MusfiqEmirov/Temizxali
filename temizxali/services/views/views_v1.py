from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.db.models import Prefetch
from django.conf import settings
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
    'ServiceDetailPage',
    'ReviewCreateView',
    'ProjectsPaginationView',
]


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
        reviews = Review.objects.filter(is_verified=True).prefetch_related(
            Prefetch('service__translations', queryset=ServiceTranslation.objects.filter(languages=languages))
        ).order_by('-created_at')
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

        paginator = Paginator(special_projects, 6)
        page = request.GET.get('page', 1)
        try:
            projects_page = paginator.page(page)
        except PageNotAnInteger:
            projects_page = paginator.page(1)
        except EmptyPage:
            projects_page = paginator.page(paginator.num_pages)
        
        return render(request, self.template_name, {
            'languages': languages,
            'background_images': background_images,
            'background_image': background_images.first() if background_images.exists() else None,
            'mottos_with_bg': mottos_with_bg,
            'services': services,
            'special_projects': projects_page,
            'statistics': statistics,
            'mottos': mottos,
            'reviews': reviews,
            'contact': contact
        })


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
            )),
            Prefetch('sales', queryset=SaleEvent.objects.filter(active=True).prefetch_related(
                Prefetch('translations', queryset=SaleEventTranslation.objects.filter(languages=languages))
            ))
        ).first()
        
       
        active_sale_events = service.sales.filter(active=True) if service else []

        contact = Contact.objects.first()
        services = Service.objects.filter(
            is_active=True,
            translations__languages=languages
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=ServiceTranslation.objects.filter(languages=languages)),
            'images'
        ).order_by('-created_at')[:6]  

        return render(request, self.template_name, {
            'languages': languages,
            'service': service,
            'translation': display_translation,
            'active_sale_events': active_sale_events,
            'contact': contact,
            'services': services,
            })


class OrderPageView(View):
    template_name = 'contact.html'
    
    def get(self, request):
        form = OrderForm()
        services = ServiceQuery.load_services()
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
        services = ServiceQuery.load_services()
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
        else:
            messages.error(request, _('Melumatlari duzgun daxil edin'))

        return render(request, self.template_name, {
            'form': form,
            'services': services,
            'contact': contact
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

