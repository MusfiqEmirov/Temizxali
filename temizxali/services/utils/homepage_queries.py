from django.utils import translation
from django.core.cache import cache
from django.db.models import Q


class HomePageQueries:
    
    @staticmethod
    def get_all_homepage_data(lang):
        
        from services.models import (
            Image, Service, SpecialProject, Motto,
            Statistic, About, Review, Contact
        )
        
        # Cache key
        cache_key = f'homepage_data_{lang}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # 1. Background images - cache-dən id-ləri, sonra real Image obyektləri
        bg_ids = cache.get('home_background_images_ids')
        if bg_ids:
            # Cache-dən id-lər var, real obyektləri gətir
            background_images = list(Image.objects.filter(
                id__in=bg_ids
            ).order_by('-created_at').only('id', 'image'))
        else:
            # Cache yoxdur, real Image obyektlərini gətir
            background_images = list(Image.objects.filter(
                is_home_page_background_image=True
            ).order_by('-created_at').only('id', 'image'))
            if background_images:
                # Yalnız id-ləri cache-ləyək
                bg_ids = [img.id for img in background_images]
                cache.set('home_background_images_ids', bg_ids, 3600)
        
        if not background_images:
            background_images = []
        
        # Background image - birinci şəkil
        background_image = background_images[0] if background_images else None
        
        # 2. Services (10 ədəd) - lazy queryset, prefetch yox
        services = Service.objects.filter(
            is_active=True,
            translations__languages=lang
        ).distinct().order_by('-created_at')[:10]
        
        # 3. Special Projects (6 ədəd) - lazy queryset, prefetch yox
        special_projects = SpecialProject.objects.filter(
            is_active=True,
            translations__languages=lang
        ).distinct().order_by('-created_at')[:6]
        
        # 4. Mottos (10 ədəd) - lazy queryset, prefetch yox
        mottos = Motto.objects.filter(
            translations__languages=lang
        ).distinct().order_by('-id')[:10]
        
        # Mottos with background - lazy evaluate
        mottos_list = list(mottos)
        mottos_with_bg = []
        if mottos_list and background_images:
            for i, m in enumerate(mottos_list):
                # background_images artıq list-dir, real Image obyektləri
                bg_img = background_images[i % len(background_images)] if background_images else None
                mottos_with_bg.append({
                    'motto': m,
                    'background_image': bg_img  # Real Image obyekti
                })
        elif mottos_list:
            for m in mottos_list:
                mottos_with_bg.append({
                    'motto': m,
                    'background_image': None
                })
        
        # 5. Statistics - lazy queryset, prefetch yox
        statistics = Statistic.objects.all()
        
        # 6. About - lazy queryset, prefetch yox
        about = About.objects.all()
        
        # 7. Reviews (10 ədəd) - lazy queryset, select_related yalnız service üçün
        reviews = Review.objects.filter(
            is_verified=True
        ).select_related('service').order_by('-created_at')[:10]
        
        # 8. Contact - bir sorğu
        contact = Contact.objects.first()
        
        # Background images wrapper - queryset-like, real Image obyektləri
        class BackgroundImagesQuerySet:
            """Background images üçün queryset-like wrapper"""
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
        
        bg_images_wrapper = BackgroundImagesQuerySet(background_images)
        
        result = {
            'languages': lang,
            'background_images': bg_images_wrapper,
            'background_image': background_image,
            'mottos_with_bg': mottos_with_bg,
            'services': services,
            'special_projects': special_projects,
            'statistics': statistics,
            'about': about,
            'reviews': reviews,
            'contact': contact
        }
        
        return result
