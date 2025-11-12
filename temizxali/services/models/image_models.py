from django.db import models

from .service_models import Service
from .special_project_models import SpecialProject
from .about_models import About


class Image(models.Model):
    service = models.ForeignKey(
        Service,
        related_name='images',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Servis'
    )
    about = models.ForeignKey(
        About,
        related_name='images',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='About'
    )
    special_project = models.ForeignKey(
        SpecialProject,
        related_name='images',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Xüsusi lahiyə'
    )
    image = models.ImageField(
        upload_to='images/',  
        verbose_name='Şəkil'
    )
    # image_name = models.CharField(
    #     max_length=50,
    #     verbose_name='Şəkil adı'
    # )
    is_home_page_background_image = models.BooleanField(
        default=False,
        verbose_name='Ana sehifesi üçün arxa plan şəkli'
    )
    is_about_page_background_image = models.BooleanField(
        default=False,
        verbose_name='Haqqımızda sehifesi üçün arxa plan şəkli'
    )
    is_calculator_page_background_image = models.BooleanField(
        default=False,
        verbose_name='Calculator sehifesi üçün arxa plan şəkli'
    )
    is_review_page_background_image = models.BooleanField(
        default=False,
        verbose_name='Comment elave et sehifesi üçün arxa plan şəkli'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Image yaradılma tarixi'
    )

    class Meta:
        verbose_name = 'Şəkil'
        verbose_name_plural = 'Şəkillər'

   