from django.db import models
from django.core.validators import MaxLengthValidator
from services.utils import LANGUAGES 

class Statistic(models.Model):
    """
    Statistikanın əsas modeli, burada yalnız ümumi identifikasiya saxlanılır.
    """
    class Meta:
        verbose_name = 'Statistika'
        verbose_name_plural = 'Statistikalar'

    def __str__(self):
        return 'Statistika'

class StatisticTranslation(models.Model):
    """
    Statistikaya aid ad və dəyəri dillərə uyğun saxlayır.
    """
    statistic = models.ForeignKey(
        Statistic,
        related_name='translations',
        on_delete=models.CASCADE,
        verbose_name='Statistika'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Statistikanın adı'
    )
    value = models.PositiveIntegerField(
        verbose_name='Dəyəri'
    )
    language = models.CharField(
        max_length=12,
        choices=LANGUAGES,
        verbose_name='Dil'
    )

    class Meta:
        verbose_name = 'Statistika tərcüməsi'
        verbose_name_plural = 'Statistika tərcümələri'

    def __str__(self):
        return f"{self.name} ({self.value})"
