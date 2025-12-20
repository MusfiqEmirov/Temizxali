from django.utils import translation
from django.core.cache import cache
from django.db.models import Q, Prefetch


class BackgroundImagesQuerySet:
    def __init__(self, images):
        self._images = list(images) if images else []
    
    def first(self):
        return self._images[0] if self._images else None
    
    def __iter__(self):
        return iter(self._images)
    
    def __len__(self):
        return len(self._images)
    
    def __getitem__(self, key):
        return self._images[key]


class HomePageQueries:
    
    @staticmethod
    def get_all_homepage_data(lang):
        
        from services.models import (
            Image, Service, SpecialProject, Motto,
            Statistic, About, Review, Contact
        )
        
        cache_key = f'homepage_data_{lang}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        bg_ids = cache.get('home_background_images_ids')
        if bg_ids:
            background_images = list(Image.objects.filter(
                id__in=bg_ids
            ).order_by('-created_at').only('id', 'image'))
        else:
            background_images = list(Image.objects.filter(
                is_home_page_background_image=True
            ).order_by('-created_at').only('id', 'image'))
            if background_images:
                bg_ids = [img.id for img in background_images]
                cache.set('home_background_images_ids', bg_ids, 3600)
        
        if not background_images:
            background_images = []
        
        background_image = background_images[0] if background_images else None
        
        from services.models import ServiceTranslation
        services = Service.objects.filter(
            is_active=True,
            translations__languages=lang
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=ServiceTranslation.objects.filter(languages=lang))
        ).order_by('-created_at')[:10]
        
        from services.models import SpecialProjectTranslation
        special_projects = SpecialProject.objects.filter(
            is_active=True,
            translations__languages=lang
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=SpecialProjectTranslation.objects.filter(languages=lang))
        ).order_by('-created_at')[:6]
        
        from services.models import MottoTranslation
        mottos = Motto.objects.filter(
            translations__languages=lang
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=MottoTranslation.objects.filter(languages=lang))
        ).order_by('-id')[:10]
        
        mottos_list = list(mottos)
        mottos_with_bg = []
        used_image_ids = set()
        if mottos_list and background_images:
            for i, m in enumerate(mottos_list):
                bg_img = background_images[i % len(background_images)] if background_images else None
                if bg_img:
                    used_image_ids.add(bg_img.id)
                mottos_with_bg.append({
                    'motto': m,
                    'background_image': bg_img
                })
        elif mottos_list:
            for m in mottos_list:
                mottos_with_bg.append({
                    'motto': m,
                    'background_image': None
                })
        
        # İstifadə olunmayan şəkilləri tap
        unused_background_images = [img for img in background_images if img.id not in used_image_ids]
        
        statistics = Statistic.objects.all()
        
        from services.models import AboutTranslation
        about = About.objects.all().prefetch_related(
            Prefetch('translations', queryset=AboutTranslation.objects.filter(languages=lang)),
            'images'
        )
        
        from services.models import Review
        reviews = Review.objects.filter(
            is_verified=True
        ).select_related('service').prefetch_related(
            Prefetch('service__translations', queryset=ServiceTranslation.objects.filter(languages=lang))
        ).order_by('-created_at')[:10]
        
        contact = Contact.objects.first()
        
        bg_images_wrapper = BackgroundImagesQuerySet(background_images)
        unused_bg_images_wrapper = BackgroundImagesQuerySet(unused_background_images)
        
        result = {
            'languages': lang,
            'background_images': bg_images_wrapper,
            'unused_background_images': unused_bg_images_wrapper,
            'background_image': background_image,
            'mottos_with_bg': mottos_with_bg,
            'services': services,
            'special_projects': special_projects,
            'statistics': statistics,
            'about': about,
            'reviews': reviews,
            'contact': contact
        }
        
        cache.set(cache_key, result, 3600)
        
        return result
