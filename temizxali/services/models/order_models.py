from django.db import models
from django.core.validators import MaxLengthValidator

from .service_models import Service


class Order(models.Model):
    services = models.ManyToManyField(
        Service,
        verbose_name='Şifariş verilən servislər'
    )
    fullname = models.CharField(
        max_length=32,
        verbose_name='Ad soyad'
    )
    # order_models.py və review_models.py
    phone_number = models.CharField(
        max_length=12,                    # indi 12 rəqəm saxlayırıq
        unique=True,                      # istəyə görə unikallıq əlavə etdim
        verbose_name='Mobil nömrə'
    )
    text = models.TextField(
        validators=[MaxLengthValidator(2000)],
        verbose_name='Mesaj'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Sifarişin verilmə tarixi'
    )

    class Meta:
        verbose_name = 'Sifariş'
        verbose_name_plural = 'Sifarişlər'
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
