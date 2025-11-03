from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator

from services.utils import SluggedModel, LANGUAGES

class Service(models.Model):
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Qiymət'
    )
    sale = models.FloatField(
        validators=[MaxValueValidator(100), MinValueValidator(1)],
        null=True,
        blank=True,
        verbose_name='Endirim'
    )
    video = models.FileField(
        upload_to='videos/',  
        null=True,
        blank=True,
        verbose_name='Video'
    )
    is_vip = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Vip'
    )
    is_premium = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Premium'
    )
    delivery = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Çatdırılma'
    )
    is_active = models.BooleanField(
        default=True,
        null=True,
        blank=True,
        verbose_name='Servis aktivliyi'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Servis yaradılma tarixi'
    )

    class Meta:
        verbose_name = 'Məhsul'
        verbose_name_plural = 'Məhsullar'
    
    def __str__(self):
        translation = self.translations.first()
        if translation:
            return translation.name
        return f'Service #{self.id}'


class ServiceTranslation(SluggedModel):
    service = models.ForeignKey(
        Service,
        related_name='translations',
        on_delete=models.CASCADE,
        verbose_name='Servis'
    )
    language = models.CharField(
        max_length=12,
        choices=LANGUAGES
    )
    name = models.CharField(
        max_length=250,
        verbose_name='Ad'
    )
    description = models.TextField(
        validators=[MaxLengthValidator(2000)],
        verbose_name='Servis haqqında'
    )

    class Meta:
        verbose_name = 'Servis Tərcüməsi'
        verbose_name_plural = 'Servis Tərcümələri'
    
    def get_slug_source(self) -> str:
        return self.name

    def __str__(self):
        return f'{self.name}'