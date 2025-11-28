from django.utils import translation
from django.core.cache import cache
from django.db.models import Prefetch


class AboutPageQueries:
    
    @staticmethod
    def get_all_about_data(lang):
        
        from services.models import (
            Image, Service, Statistic, About, Contact,
            AboutTranslation, ServiceTranslation
        )
        
        cache_key = f'about_data_{lang}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        about = About.objects.all().distinct().prefetch_related(
            Prefetch('translations', queryset=AboutTranslation.objects.filter(languages=lang)),
            'images'
        )
        about_item = about.first() if about.exists() else None
        
        statistics = Statistic.objects.prefetch_related('translations').all()
        
        contact = Contact.objects.first()
        
        services = Service.objects.filter(
            is_active=True,
            translations__languages=lang
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=ServiceTranslation.objects.filter(languages=lang))
        ).order_by('-created_at')
        
        about_background_image = Image.objects.filter(
            is_about_page_background_image=True
        ).first()
        
        result = {
            'about': about,
            'about_item': about_item,
            'statistics': statistics,
            'active_lang': lang,
            'contact': contact,
            'services': services,
            'about_background_image': about_background_image,
        }
        
        cache.set(cache_key, result, 3600)
        
        return result

