from django.db import models
from django.core.validators import MaxLengthValidator

from services.utils import LANGUAGES


class SpecialProject(models.Model):
    url = models.URLField(
        null=True,
        blank=True,
        verbose_name='Url'
    )
    is_active = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Lahiyə aktivliyi'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Lahiyə yaradılma tarixi'
    )

    class Meta:
        verbose_name = 'Xüsusi Lahiyə'
        verbose_name_plural = 'Xüsusi Lahiyələr'
        ordering = ('-created_at',)

    def __str__(self):
        translation = self.translations.first()
        return translation.description[:20] if translation else "No description"


class SpecialProjectTranslation(models.Model):
    project = models.ForeignKey(
        SpecialProject,
        related_name='translations',
        on_delete=models.CASCADE,
        verbose_name='Xüsusi layihə'
    )
    languages = models.CharField(
        max_length=12,
        choices=LANGUAGES,
        verbose_name='Dil'
    )
    description = models.CharField(
        max_length=350,
        validators=[MaxLengthValidator(2000)],
        verbose_name='Xüsusi layihə haqqında məlumat'
    )

    class Meta:
        verbose_name = 'Xüsusi layihə tərcüməsi'
        verbose_name_plural = 'Xüsusi layihə tərcümələri'

    def __str__(self):
        return f'{self.description[:20]} ({self.languages})'