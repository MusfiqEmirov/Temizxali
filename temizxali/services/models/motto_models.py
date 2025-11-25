from django.db import models
from django.core.validators import MaxLengthValidator

from services.utils import LANGUAGES


class Motto(models.Model):

    class Meta:
        verbose_name = 'Deviz'
        verbose_name_plural = 'Devizlər'

    def __str__(self):
        return 'Motto'


class MottoTranslation(models.Model):
    motto = models.ForeignKey(
        Motto,
        on_delete=models.CASCADE,
        related_name='translations',
        verbose_name='Deviz'
    )
    text = models.TextField(
        validators=[MaxLengthValidator(2000)],
        verbose_name='Deviz cümləsi'
    )
    languages = models.CharField(
        max_length=12,
        choices=LANGUAGES,
        verbose_name='Dil'
    )

    class Meta:
        verbose_name = 'Deviz tərcüməsi'
        verbose_name = 'Deviz tərcümələri'

    def __str__(self):
        return self.text[:20]