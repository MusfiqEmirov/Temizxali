from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from services.models import About, Service, Statistic, Review, Motto, MottoTranslation, Image, SpecialProject


@receiver(post_save, sender=About)
@receiver(post_delete, sender=About)
def clear_about_cache(sender, **kwargs):
    cache.clear()  # bütün keş silinir


@receiver(post_save, sender=Service)
@receiver(post_delete, sender=Service)
def clear_service_cache(sender, **kwargs):
    cache.clear()


@receiver(post_save, sender=Statistic)
def clear_statistic_cache(sender, **kwargs):
    cache.clear()


@receiver(post_save, sender=Motto)
@receiver(post_delete, sender=Motto)
@receiver(post_save, sender=MottoTranslation)
@receiver(post_delete, sender=MottoTranslation)
def clear_motto_cache(sender, **kwargs):
    cache.clear()


@receiver(post_save, sender=Image)
@receiver(post_delete, sender=Image)
def clear_image_cache(sender, **kwargs):
    # Background image və ya hər hansı image dəyişəndə cache sil
    instance = kwargs.get('instance')
    if instance and (instance.is_background_image or instance.image_name == 'home_page_background'):
        cache.clear()


@receiver(post_save, sender=SpecialProject)
@receiver(post_delete, sender=SpecialProject)
def clear_special_project_cache(sender, **kwargs):
    cache.clear()


