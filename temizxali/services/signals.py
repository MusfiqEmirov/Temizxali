from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from services.models import About, Service, Statistic, Review


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


