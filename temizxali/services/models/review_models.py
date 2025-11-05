from django.db import models
from django.core.validators import MaxLengthValidator

from .service_models import Service


class Review(models.Model):
    services = models.ManyToManyField(
        Service,
        verbose_name='Rəy verilən servislər'
    )
    fullname = models.CharField(
        max_length=32,
        verbose_name='Ad soyad'
    )
    phone_number = models.CharField(
        max_length=10,
        verbose_name='Mobil nömrə'
    )
    text = models.TextField(
        validators=[MaxLengthValidator(2000)],
        verbose_name='Mesaj'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Rəyin təsdiqlənməsi'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Rəyin yaradılma tarixi'
    )

    class Meta:
        verbose_name = 'Rəy'
        verbose_name_plural = 'Rəylər'
        ordering = ('-created_at',)
    
    def __str__(self):
       return f'{self.phone_number}: {self.text[:20]}'
