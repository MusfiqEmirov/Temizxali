from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator

from services.utils import MEASURE_TYPE_CHOICES, LANGUAGES
from services.models import Service



class SaleEvent(models.Model):
    service = models.ManyToManyField(
        Service, 
        related_name='sales', 
        verbose_name='Servis'
    )
    sale = models.FloatField(
        validators=[MaxValueValidator(100), MinValueValidator(1)],
        null=True,
        blank=True,
        verbose_name='Endirim faizi'
    )
    min_quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Endirimin aktif olacağı dəyər'
    )
    active = models.BooleanField(
        default=True, 
        verbose_name='Aktiv'
    )
    
    class Meta:
        verbose_name = 'Endirim kampaniyası'
        verbose_name_plural = 'Endirim kampaniyaları'

    def __str__(self):
        translation = self.translations.first()
        if translation:
            return translation.name
        return f'SaleEvent #{self.id}'
    

class SaleEventTranslation(models.Model):
    sale = models.ForeignKey(
        SaleEvent,
        on_delete=models.CASCADE, 
        related_name='translations', 
        verbose_name='Endirim eventi'
    )
    languages = models.CharField(
        max_length=12,
        choices=LANGUAGES,
        null=True,
        blank=True,
        verbose_name='Dillər'
    )
    name = models.CharField(
        max_length=50, 
        verbose_name='Aksiya Adı'
    )
    description = models.TextField(
        validators=[MaxLengthValidator(350)],
        verbose_name='Aksiya haqqında'
    )
    class Meta:
        verbose_name = 'Endirim kampaniyası təcüməsi'
        verbose_name_plural = 'Endirim kampaniyaları tərcümələri'

    def __str__(self):
        return self.name