from django.utils import translation
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.core.cache import cache


class ServiceDetailQueries:
    
    @staticmethod
    def get_service_detail_data(lang, service_slug):
        
        cache_key = f'service_detail_data_{lang}_{service_slug}'
        cached_data = cache.get(cache_key)
        
        from services.models import (
            Service, ServiceTranslation, ServiceVariant,
            ServiceVariantTranslation, SaleEvent, SaleEventTranslation,
            Contact, Image
        )
        
        contact = Contact.objects.first()
        
        if cached_data:
            cached_data['contact'] = contact
            return cached_data
        
        translation_obj = get_object_or_404(
            ServiceTranslation,
            slug=service_slug
        )
        service = translation_obj.service
        
        current_lang_translation = service.translations.filter(
            languages=lang
        ).first()
        display_translation = current_lang_translation if current_lang_translation else translation_obj
        
        service = Service.objects.filter(
            id=service.id
        ).prefetch_related(
            Prefetch('translations', queryset=ServiceTranslation.objects.filter(
                languages=lang
            )),
            'images',
            Prefetch('variants', queryset=ServiceVariant.objects.all().prefetch_related(
                Prefetch('translations', queryset=ServiceVariantTranslation.objects.filter(languages=lang)),
                'images'
            )),
            Prefetch('sales', queryset=SaleEvent.objects.filter(active=True).prefetch_related(
                Prefetch('translations', queryset=SaleEventTranslation.objects.filter(languages=lang))
            ))
        ).first()
        
        active_sale_events = service.sales.filter(active=True) if service else []
        
        services = Service.objects.filter(
            is_active=True,
            translations__languages=lang
        ).distinct().prefetch_related(
            Prefetch('translations', queryset=ServiceTranslation.objects.filter(languages=lang)),
            'images'
        ).order_by('-created_at')[:6]
        
        result = {
            'languages': lang,
            'service': service,
            'translation': display_translation,
            'active_sale_events': active_sale_events,
            'contact': contact,
            'services': services,
        }
        
        cache_result = result.copy()
        cache_result['contact'] = None  
        cache.set(cache_key, cache_result, 3600)
        
        return result

