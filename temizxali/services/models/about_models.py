from django.db import models
from django.core.validators import MaxLengthValidator

from services.utils import LANGUAGES


class About(models.Model):
    image = models.ImageField(
        upload_to='about-image/',  
        null=True,
        blank=True,
        verbose_name='Haqqımızda arxa plan şəkili'
    )

    class Mete:
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
        verbose_name = 'Haqqımızda tərcümələri'

    def __str__(self):
        return self.about[:20]


