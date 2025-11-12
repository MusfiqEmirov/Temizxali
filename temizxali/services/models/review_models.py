from django.db import models
from django.core.validators import MaxLengthValidator

from .service_models import Service
from services.utils.normalize_phone_number import normalize_az_phone


class Review(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Service',
    )
    fullname = models.CharField(
        max_length=32,
        verbose_name='Ad soyad'
    )
    phone_number = models.CharField(
        max_length=12,
        verbose_name='Mobil nömrə'
    )
    text = models.TextField(
        validators=[MaxLengthValidator(140)],
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

    def save(self, *args, **kwargs):
        if self.phone_number:
            from services.utils.normalize_phone_number import normalize_az_phone
            normalized = normalize_az_phone(self.phone_number)
            if normalized:
                self.phone_number = normalized
            else:
                raise ValueError("Düzgün Azərbaycan mobil nömrəsi deyil.")
        super().save(*args, **kwargs)