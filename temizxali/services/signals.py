from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from services.utils.cache_invalidation import CacheInvalidation

from services.models import (
    Image, Service, SpecialProject, Motto, Statistic, About, Review, Contact,
    ServiceTranslation, SpecialProjectTranslation, MottoTranslation,
    StatisticTranslation, AboutTranslation,
    ServiceVariant, ServiceVariantTranslation, SaleEvent, SaleEventTranslation,
)
from services.utils import convert_to_webp, run_async


@receiver(post_save, sender=Image)
def handle_webp(sender, instance, created, **kwargs):
    if created:
        run_async(convert_to_webp, instance)


@receiver([post_save, post_delete], sender=Image)
def invalidate_cache_on_image_change(sender, instance, **kwargs):
    """Invalidate cache when Image is changed or deleted"""
    CacheInvalidation.clear_homepage_cache()
    CacheInvalidation.clear_about_cache()
    CacheInvalidation.clear_projects_cache()
    if instance.service:
        if instance.service.translations.exists():
            slugs = instance.service.translations.values_list('slug', flat=True)
            for slug in slugs:
                CacheInvalidation.clear_service_detail_cache(service_slug=slug)


@receiver([post_save, post_delete], sender=Service)
def invalidate_cache_on_service_change(sender, instance, **kwargs):
    """Invalidate cache when Service is changed or deleted"""
    CacheInvalidation.clear_homepage_cache()
    CacheInvalidation.clear_about_cache()
    CacheInvalidation.clear_projects_cache()
    if instance.translations.exists():
        slugs = instance.translations.values_list('slug', flat=True)
        for slug in slugs:
            CacheInvalidation.clear_service_detail_cache(service_slug=slug)


@receiver([post_save, post_delete], sender=ServiceTranslation)
def invalidate_cache_on_service_translation_change(sender, instance, **kwargs):
    """Invalidate cache when ServiceTranslation is changed or deleted"""
    CacheInvalidation.clear_homepage_cache()
    CacheInvalidation.clear_about_cache()
    CacheInvalidation.clear_projects_cache()
    CacheInvalidation.clear_service_detail_cache(service_slug=instance.slug)


@receiver([post_save, post_delete], sender=ServiceVariant)
def invalidate_cache_on_service_variant_change(sender, instance, **kwargs):
    """Invalidate cache when ServiceVariant is changed or deleted"""
    if instance.service and instance.service.translations.exists():
        slugs = instance.service.translations.values_list('slug', flat=True)
        for slug in slugs:
            CacheInvalidation.clear_service_detail_cache(service_slug=slug)


@receiver([post_save, post_delete], sender=ServiceVariantTranslation)
def invalidate_cache_on_service_variant_translation_change(sender, instance, **kwargs):
    """Invalidate cache when ServiceVariantTranslation is changed or deleted"""
    if instance.variant and instance.variant.service and instance.variant.service.translations.exists():
        slugs = instance.variant.service.translations.values_list('slug', flat=True)
        for slug in slugs:
            CacheInvalidation.clear_service_detail_cache(service_slug=slug)


@receiver([post_save, post_delete], sender=SaleEvent)
def invalidate_cache_on_sale_event_change(sender, instance, **kwargs):
    """Invalidate cache when SaleEvent is changed or deleted"""
    CacheInvalidation.clear_service_detail_cache()


@receiver([post_save, post_delete], sender=SaleEventTranslation)
def invalidate_cache_on_sale_event_translation_change(sender, instance, **kwargs):
    """Invalidate cache when SaleEventTranslation is changed or deleted"""
    CacheInvalidation.clear_service_detail_cache()


@receiver([post_save, post_delete], sender=SpecialProject)
def invalidate_cache_on_special_project_change(sender, instance, **kwargs):
    """Invalidate cache when SpecialProject is changed or deleted"""
    CacheInvalidation.clear_homepage_cache()
    CacheInvalidation.clear_projects_cache()


@receiver([post_save, post_delete], sender=SpecialProjectTranslation)
def invalidate_cache_on_special_project_translation_change(sender, instance, **kwargs):
    """Invalidate cache when SpecialProjectTranslation is changed or deleted"""
    CacheInvalidation.clear_homepage_cache()
    CacheInvalidation.clear_projects_cache()


@receiver([post_save, post_delete], sender=Motto)
def invalidate_cache_on_motto_change(sender, instance, **kwargs):
    """Invalidate cache when Motto is changed or deleted"""
    CacheInvalidation.clear_homepage_cache()


@receiver([post_save, post_delete], sender=MottoTranslation)
def invalidate_cache_on_motto_translation_change(sender, instance, **kwargs):
    """Invalidate cache when MottoTranslation is changed or deleted"""
    CacheInvalidation.clear_homepage_cache()


@receiver([post_save, post_delete], sender=Statistic)
def invalidate_cache_on_statistic_change(sender, instance, **kwargs):
    """Invalidate cache when Statistic is changed or deleted"""
    CacheInvalidation.clear_homepage_cache()
    CacheInvalidation.clear_about_cache()


@receiver([post_save, post_delete], sender=StatisticTranslation)
def invalidate_cache_on_statistic_translation_change(sender, instance, **kwargs):
    """Invalidate cache when StatisticTranslation is changed or deleted"""
    CacheInvalidation.clear_homepage_cache()
    CacheInvalidation.clear_about_cache()


@receiver([post_save, post_delete], sender=About)
def invalidate_cache_on_about_change(sender, instance, **kwargs):
    """Invalidate cache when About is changed or deleted"""
    CacheInvalidation.clear_homepage_cache()
    CacheInvalidation.clear_about_cache()


@receiver([post_save, post_delete], sender=AboutTranslation)
def invalidate_cache_on_about_translation_change(sender, instance, **kwargs):
    """Invalidate cache when AboutTranslation is changed or deleted"""
    CacheInvalidation.clear_homepage_cache()
    CacheInvalidation.clear_about_cache()


@receiver([post_save, post_delete], sender=Review)
def invalidate_cache_on_review_change(sender, instance, **kwargs):
    """Invalidate cache when Review is changed or deleted"""
    CacheInvalidation.clear_homepage_cache()


@receiver([post_save, post_delete], sender=Contact)
def invalidate_cache_on_contact_change(sender, instance, **kwargs):
    """Invalidate cache when Contact is changed or deleted"""
    CacheInvalidation.clear_homepage_cache()
    CacheInvalidation.clear_about_cache()
    CacheInvalidation.clear_projects_cache()
    CacheInvalidation.clear_service_detail_cache()

