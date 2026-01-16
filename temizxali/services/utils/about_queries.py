from django.utils import translation
from django.core.cache import cache
from django.db.models import Prefetch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class AboutPageQueries:
    
    @staticmethod
    def get_all_about_data(lang, page=1, per_page=6):
        
        from services.models import (
            Image, Service, Statistic, About, Contact,
            AboutTranslation, ServiceTranslation, SpecialProject,
            SpecialProjectTranslation
        )
        
        cache_key = f'about_data_{lang}_page_{page}'
        cached_data = cache.get(cache_key)
        
        contact = Contact.objects.first()
        
        if cached_data:
            cached_data['contact'] = contact
            return cached_data
        
        about = About.objects.all().distinct().prefetch_related(
            Prefetch('translations', queryset=AboutTranslation.objects.filter(languages=lang)),
            'images'
        )
        about_item = about.first() if about.exists() else None
        
        statistics = Statistic.objects.prefetch_related('translations').all()
        
        services = Service.objects.filter(
            is_active=True,
            translations__languages=lang
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=ServiceTranslation.objects.filter(languages=lang))
        ).order_by('-created_at')
        
        about_background_image = Image.objects.filter(
            is_about_page_background_image=True
        ).first()
        
        special_projects = SpecialProject.objects.filter(
            is_active=True,
            translations__languages=lang
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=SpecialProjectTranslation.objects.filter(languages=lang)),
            'images'
        ).order_by('-created_at')
        
        paginator = Paginator(special_projects, per_page)
        try:
            projects_page = paginator.page(page)
        except PageNotAnInteger:
            projects_page = paginator.page(1)
        except EmptyPage:
            projects_page = paginator.page(paginator.num_pages)
        
        result = {
            'about': about,
            'about_item': about_item,
            'statistics': statistics,
            'active_lang': lang,
            'contact': contact,
            'services': services,
            'about_background_image': about_background_image,
            'special_projects': projects_page,
        }
        
        cache_result = result.copy()
        cache_result['contact'] = None  
        cache.set(cache_key, cache_result, 3600)
        
        return result

