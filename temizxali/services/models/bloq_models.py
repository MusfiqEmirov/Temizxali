from django.db import models
from django.core.validators import MaxLengthValidator
from ckeditor.fields import RichTextField

from services.utils import LANGUAGES, SluggedModel


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
    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Baxış sayı'
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


class BloqTranslation(SluggedModel):
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
    description = models.CharField(
        max_length=250,
        validators=[MaxLengthValidator(250)],
        null=True,
        blank=True,
        verbose_name='Bloq haqqında başlanğıc cümləsi'
    )
    content = RichTextField(
        max_length=10000,
        validators=[MaxLengthValidator(10000)],
        null=True,
        blank=True,
        verbose_name='Bloq haqqında'
    )
  
    class Meta:
        verbose_name = 'Bloq'
        verbose_name_plural = 'Bloq tərcümələri'

    def get_slug_source(self) -> str:
        return self.name

    def __str__(self):
        if self.description:
            return f'{self.description[:20]} ({self.languages})'
        else:
            return f'{self.name} ({self.languages})'