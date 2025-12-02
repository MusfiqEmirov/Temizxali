from django.db import models
from PIL import Image as PilImage
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

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

    @property
    def webp_url(self):
        return self.image.url

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        update_fields = kwargs.get('update_fields', [])
        image_changed = is_new or 'image' in update_fields or not update_fields
        
        original_image_name = None
        if image_changed and self.image:
            original_image_name = self.image.name
        
        super().save(*args, **kwargs)
        
        if image_changed and self.image and hasattr(self.image, 'path'):
            try:
                image_name_lower = self.image.name.lower()
                is_webp = image_name_lower.endswith('.webp')
                
                if is_webp:
                    try:
                        img = PilImage.open(self.image.path)
                        if img.format == 'WEBP':
                            return
                    except Exception:
                        pass
                
                img = PilImage.open(self.image.path)

                if img.mode != "RGB":
                    img = img.convert("RGB")

                buffer = BytesIO()
                img.save(buffer, format="WEBP")
                buffer.seek(0)

                webp_name = self.image.name.rsplit(".", 1)[0] + ".webp"
                
                self.image.save(webp_name, ContentFile(buffer.read()), save=False)
                buffer.close()
                
                if original_image_name and original_image_name != webp_name:
                    try:
                        storage = default_storage
                        if storage.exists(original_image_name):
                            storage.delete(original_image_name)
                    except Exception:
                        pass
                
                super().save(update_fields=['image'])
            except Exception:
                pass