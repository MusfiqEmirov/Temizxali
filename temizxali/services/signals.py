from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
import logging
from services.utils.cache_invalidation import CacheInvalidation

from services.models import (
    Image, Service, SpecialProject, Motto, Statistic, About, Review, Contact,
    ServiceTranslation, SpecialProjectTranslation, MottoTranslation,
    StatisticTranslation, AboutTranslation,
    ServiceVariant, ServiceVariantTranslation, SaleEvent, SaleEventTranslation,
)

logger = logging.getLogger(__name__)


@receiver([post_save, post_delete], sender=Image)
def invalidate_cache_on_image_change(sender, instance, **kwargs):
    """Invalidate cache when Image is changed or deleted"""
    CacheInvalidation.clear_homepage_cache()
    CacheInvalidation.clear_about_cache()
    CacheInvalidation.clear_projects_cache()
    try:
        service = instance.service
        if service:
            translations = service.translations.all()
            for translation in translations:
                if translation.slug:
                    CacheInvalidation.clear_service_detail_cache(service_slug=translation.slug)
    except ObjectDoesNotExist:
        pass


@receiver(pre_delete, sender=Service)
def delete_service_images(sender, instance, **kwargs):
    try:
        images = list(instance.images.all())
        count = len(images)
        if count > 0:
            logger.info(f"[SERVICE DELETE] {count} images found, deleting files... (Service ID: {instance.id})")
            for image in images:
                image.delete_files()
            logger.info(f"[SERVICE DELETE] {count} image files successfully deleted (Service ID: {instance.id})")
    except Exception as e:
        logger.error(f"[SERVICE DELETE] Error occurred (Service ID: {instance.id}): {e}")


@receiver(pre_delete, sender=SpecialProject)
def delete_special_project_images(sender, instance, **kwargs):
    try:
        images = list(instance.images.all())
        count = len(images)
        if count > 0:
            logger.info(f"[SPECIAL_PROJECT DELETE] {count} images found, deleting files... (SpecialProject ID: {instance.id})")
            for image in images:
                image.delete_files()
            logger.info(f"[SPECIAL_PROJECT DELETE] {count} image files successfully deleted (SpecialProject ID: {instance.id})")
    except Exception as e:
        logger.error(f"[SPECIAL_PROJECT DELETE] Error occurred (SpecialProject ID: {instance.id}): {e}")


@receiver(pre_delete, sender=About)
def delete_about_images(sender, instance, **kwargs):
    try:
        images = list(instance.images.all())
        count = len(images)
        if count > 0:
            logger.info(f"[ABOUT DELETE] {count} images found, deleting files... (About ID: {instance.id})")
            for image in images:
                image.delete_files()
            logger.info(f"[ABOUT DELETE] {count} image files successfully deleted (About ID: {instance.id})")
    except Exception as e:
        logger.error(f"[ABOUT DELETE] Error occurred (About ID: {instance.id}): {e}")


@receiver([post_save, post_delete], sender=Service)
def invalidate_cache_on_service_change(sender, instance, **kwargs):
    """Invalidate cache when Service is changed or deleted"""
    CacheInvalidation.clear_homepage_cache()
    CacheInvalidation.clear_about_cache()
    CacheInvalidation.clear_projects_cache()
    # Service detail cache-i clear et
    if instance:
        translations = instance.translations.all()
        for translation in translations:
            if translation.slug:
                CacheInvalidation.clear_service_detail_cache(service_slug=translation.slug)


@receiver([post_save, post_delete], sender=ServiceTranslation)
def invalidate_cache_on_service_translation_change(sender, instance, **kwargs):
    """Invalidate cache when ServiceTranslation is changed or deleted"""
    CacheInvalidation.clear_homepage_cache()
    CacheInvalidation.clear_about_cache()
    CacheInvalidation.clear_projects_cache()
    # Service detail cache-i clear et
    if instance and instance.slug:
        CacheInvalidation.clear_service_detail_cache(service_slug=instance.slug)


@receiver([post_save, post_delete], sender=ServiceVariant)
def invalidate_cache_on_service_variant_change(sender, instance, **kwargs):
    """Invalidate cache when ServiceVariant is changed or deleted"""
    try:
        service = instance.service
        if service:
            translations = service.translations.all()
            for translation in translations:
                if translation.slug:
                    CacheInvalidation.clear_service_detail_cache(service_slug=translation.slug)
    except ObjectDoesNotExist:
        pass


@receiver([post_save, post_delete], sender=ServiceVariantTranslation)
def invalidate_cache_on_service_variant_translation_change(sender, instance, **kwargs):
    """Invalidate cache when ServiceVariantTranslation is changed or deleted"""
    try:
        variant = instance.variant
        if variant:
            try:
                service = variant.service
                if service:
                    translations = service.translations.all()
                    for translation in translations:
                        if translation.slug:
                            CacheInvalidation.clear_service_detail_cache(service_slug=translation.slug)
            except ObjectDoesNotExist:
                pass
    except ObjectDoesNotExist:
        pass


@receiver([post_save, post_delete], sender=SaleEvent)
def invalidate_cache_on_sale_event_change(sender, instance, **kwargs):
    """Invalidate cache when SaleEvent is changed or deleted"""
    try:
        service = instance.service
        if service:
            translations = service.translations.all()
            for translation in translations:
                if translation.slug:
                    CacheInvalidation.clear_service_detail_cache(service_slug=translation.slug)
    except ObjectDoesNotExist:
        pass


@receiver([post_save, post_delete], sender=SaleEventTranslation)
def invalidate_cache_on_sale_event_translation_change(sender, instance, **kwargs):
    """Invalidate cache when SaleEventTranslation is changed or deleted"""
    try:
        sale_event = instance.sale
        if sale_event:
            service = sale_event.service
            if service:
                translations = service.translations.all()
                for translation in translations:
                    if translation.slug:
                        CacheInvalidation.clear_service_detail_cache(service_slug=translation.slug)
    except ObjectDoesNotExist:
        pass


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

