from django.utils import translation
from django.core.cache import cache
from django.db.models import Prefetch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ProjectsPageQueries:
    
    @staticmethod
    def get_all_projects_data(lang, page=1, per_page=6):
        
        from services.models import (
            SpecialProject, SpecialProjectTranslation, Service,
            ServiceTranslation, Contact, Image
        )
        
        cache_key = f'projects_data_{lang}_page_{page}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
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
        
        contact = Contact.objects.first()
        
        services = Service.objects.filter(
            is_active=True,
            translations__languages=lang
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=ServiceTranslation.objects.filter(languages=lang))
        ).order_by('-created_at')[:10]
        
        projects_background_image = Image.objects.filter(
            is_projects_page_background_image=True
        ).first()
        
        result = {
            'languages': lang,
            'special_projects': projects_page,
            'contact': contact,
            'services': services,
            'projects_background_image': projects_background_image,
        }
        
        cache.set(cache_key, result, 3600)
        
        return result

