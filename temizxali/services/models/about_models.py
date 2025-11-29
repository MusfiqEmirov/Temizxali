from django.db import models
from django.core.validators import MaxLengthValidator

from services.utils import LANGUAGES


class About(models.Model):
    experience_years = models.PositiveSmallIntegerField(
        verbose_name='Xidmət etdiyiniz il'
    )

    class Meta:
        verbose_name = 'Haqqımızda'
        verbose_name_plural = 'Haqqımızda'

    def __str__(self):
        return 'Haqqımızda'


class AboutTranslation(models.Model):
    about = models.ForeignKey(
        About,
        related_name='translations',
        on_delete=models.CASCADE,
        verbose_name='Haqqımızda'
    )
    languages = models.CharField(
        max_length=12,
        choices=LANGUAGES,
        verbose_name='Dil'
    )
    main_title = models.CharField(
        null=True,
        blank=True,
        max_length=120,
        verbose_name='Əsas başlıq'
    )
    highlight_title_one = models.CharField(
        null=True,
        blank=True,
        max_length=80,
        verbose_name='Sol üst ilk başlıq'
    )
    highlight_title_two = models.CharField(
        null=True,
        blank=True,
        max_length=80,
        verbose_name='Sol üst ikinci başlıq'
    )
    highlight_description_one = models.TextField(
        null=True,
        blank=True,
        validators=[MaxLengthValidator(200)],
        verbose_name='Sol üst ilk açıqlama'
    )
    highlight_description_two = models.TextField(
        null=True,
        blank=True,
        validators=[MaxLengthValidator(200)],
        verbose_name='Sol üst ikinci açıqlama'
    )
    description = models.TextField(
        validators=[MaxLengthValidator(2000)],
        verbose_name='Servis haqqında'
    )
    languages = models.CharField(
        max_length=12,
        choices=LANGUAGES,
        verbose_name='Dil'
    )

    class Meta:
        verbose_name = 'Haqqımızda tərcüməsi'
        verbose_name_plural = 'Haqqımızda tərcümələri'

    def __str__(self):
        return self.description[:20]


