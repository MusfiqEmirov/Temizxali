from django.db import models
from django.core.validators import MaxLengthValidator

from services.utils import LANGUAGES


class Bloq(models.Model):
    url = models.URLField(
        null=True,
        blank=True,
        verbose_name='Url'
    )
    is_active = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Bloq aktivliyi'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Bloq yaradılma tarixi'
    )

    class Meta:
        verbose_name = 'Bloq'
        verbose_name_plural = 'Bloqlar'
        ordering = ('-created_at',)

    def __str__(self):
        translation = self.translations.first()
        return translation.description[:20] if translation else "No description"


class BloqTranslation(models.Model):
    bloq = models.ForeignKey(
        Bloq,
        related_name='translations',
        on_delete=models.CASCADE,
        verbose_name='Bloq'
    )
    name = models.CharField(
        max_length=80,
        verbose_name='Bloq növ adı'
    )
    languages = models.CharField(
        max_length=12,
        choices=LANGUAGES,
        verbose_name='Dil'
    )
    header = models.CharField(
        max_length=250,
        validators=[MaxLengthValidator(250)],
        null=True,
        blank=True,
        verbose_name='Bloq haqqında başlanğıc cümləsi'
    )

    description = models.CharField(
        max_length=5000,
        validators=[MaxLengthValidator(5000)],
        null=True,
        blank=True,
        verbose_name='Bloq haqqında'
    )

    class Meta:
        verbose_name = 'Bloq'
        verbose_name_plural = 'Bloq tərcümələri'

    def __str__(self):
        return f'{self.description[:20]} ({self.languages})'