from django.db import models
from PIL import Image as PilImage
from io import BytesIO
from django.core.files.base import ContentFile
import uuid
import os

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
    is_testimonial_page_background_image = models.BooleanField(
        default=False,
        verbose_name='Rəylər sehifesi üçün arxa plan şəkli'
    )
    is_projects_page_background_image = models.BooleanField(
        default=False,
        verbose_name='Xüsusi Layihələr sehifesi üçün arxa plan şəkli'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Image yaradılma tarixi'
    )

    class Meta:
        verbose_name = 'Şəkil'
        verbose_name_plural = 'Şəkillər'

   

    def save(self, *args, **kwargs):
        old_image = None
        if self.pk:
            try:
                old_image = Image.objects.get(pk=self.pk).image
            except Image.DoesNotExist:
                pass

        if not self.pk or (old_image and old_image != self.image):
            ext = os.path.splitext(self.image.name)[1]
            new_name = f"{uuid.uuid4().hex}{ext}"
            self.image.name = new_name

        super().save(*args, **kwargs)

        img = PilImage.open(self.image.path)

        if img.mode != "RGB":
            img = img.convert("RGB")

        max_width = 1920
        if img.width > max_width:
            ratio = max_width / float(img.width)
            height = int(float(img.height) * ratio)
            img = img.resize((max_width, height), PilImage.LANCZOS)

        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=70, optimize=True)
        buffer.seek(0)
        self.image.save(self.image.name, ContentFile(buffer.read()), save=False)
        buffer.close()

        webp_name = f"{os.path.splitext(self.image.name)[0]}.webp"
        webp_buffer = BytesIO()
        img.save(webp_buffer, format='WebP', quality=70, optimize=True)
        webp_buffer.seek(0)
        self.image.storage.save(webp_name, ContentFile(webp_buffer.read()))
        webp_buffer.close()

        super().save(*args, **kwargs)

