from django.core.cache import cache
from django.conf import settings


class CacheInvalidation:
    
    LANGUAGES = ['az', 'ru']
    
    @staticmethod
    def clear_homepage_cache():
        for lang in CacheInvalidation.LANGUAGES:
            cache.delete(f'homepage_data_{lang}')
        cache.delete('home_background_images_ids')
    
    @staticmethod
    def clear_about_cache():
        for lang in CacheInvalidation.LANGUAGES:
            cache.delete(f'about_data_{lang}')
    
    @staticmethod
    def clear_service_detail_cache(service_slug=None):
        if service_slug:
            for lang in CacheInvalidation.LANGUAGES:
                cache.delete(f'service_detail_data_{lang}_{service_slug}')
        else:
            from services.models import ServiceTranslation
            all_slugs = ServiceTranslation.objects.values_list('slug', flat=True).distinct()
            for slug in all_slugs:
                for lang in CacheInvalidation.LANGUAGES:
                    cache.delete(f'service_detail_data_{lang}_{slug}')
    
    @staticmethod
    def clear_projects_cache():
        from services.models import SpecialProject
        total_projects = SpecialProject.objects.filter(is_active=True).count()
        per_page = 6
        total_pages = (total_projects // per_page) + 1
        
        for lang in CacheInvalidation.LANGUAGES:
            for page in range(1, total_pages + 1):
                cache.delete(f'projects_data_{lang}_page_{page}')
    
    @staticmethod
    def clear_all_cache():
        CacheInvalidation.clear_homepage_cache()
        CacheInvalidation.clear_about_cache()
        CacheInvalidation.clear_service_detail_cache()
        CacheInvalidation.clear_projects_cache()

