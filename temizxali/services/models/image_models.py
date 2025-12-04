from django.db import models
from django.core.files.storage import default_storage
import logging

from .service_models import Service
from .special_project_models import SpecialProject
from .about_models import About

logger = logging.getLogger(__name__)


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

    def delete_files(self):
        if not self.image:
            return
        
        image_name = self.image.name
        image_id = self.pk
        
        logger.info(f"[IMAGE DELETE FILES] Deleting files (Image ID: {image_id}, File: {image_name})")
        
        try:
            storage = default_storage
            
            if image_name.lower().endswith('.webp'):
                logger.info(f"[IMAGE DELETE FILES] WebP file found: {image_name}")
                base_name = image_name.rsplit('.', 1)[0]
                possible_extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
                for ext in possible_extensions:
                    original_name = base_name + ext
                    if storage.exists(original_name):
                        try:
                            storage.delete(original_name)
                            logger.info(f"[IMAGE DELETE FILES] Original file deleted: {original_name}")
                        except Exception as e:
                            logger.error(f"[IMAGE DELETE FILES] Error deleting original file ({original_name}): {e}")
                
                if storage.exists(image_name):
                    storage.delete(image_name)
                    logger.info(f"[IMAGE DELETE FILES] WebP file deleted: {image_name}")
                else:
                    logger.warning(f"[IMAGE DELETE FILES] WebP file not found: {image_name}")
            else:
                logger.info(f"[IMAGE DELETE FILES] Original format file found: {image_name}")
                webp_name = image_name.rsplit('.', 1)[0] + '.webp'
                if storage.exists(webp_name):
                    try:
                        storage.delete(webp_name)
                        logger.info(f"[IMAGE DELETE FILES] WebP version deleted: {webp_name}")
                    except Exception as e:
                        logger.error(f"[IMAGE DELETE FILES] Error deleting WebP version ({webp_name}): {e}")
                
                if storage.exists(image_name):
                    storage.delete(image_name)
                    logger.info(f"[IMAGE DELETE FILES] Original file deleted: {image_name}")
                else:
                    logger.warning(f"[IMAGE DELETE FILES] Original file not found: {image_name}")
            
            logger.info(f"[IMAGE DELETE FILES] Files successfully deleted (Image ID: {image_id})")
        except Exception as e:
            logger.error(f"[IMAGE DELETE FILES] Error occurred (Image ID: {image_id}): {e}")

    # def save(self, *args, **kwargs):
    #     is_new = self.pk is None
    #     update_fields = kwargs.get('update_fields', [])
    #     image_changed = is_new or 'image' in update_fields or not update_fields

    #     old_image_name = None
    #     if not is_new and self.pk and image_changed:
    #         try:
    #             old_instance = Image.objects.get(pk=self.pk)
    #             if old_instance.image:
    #                 old_image_name = old_instance.image.name
    #                 logger.info(f"[IMAGE SAVE] Old file found: {old_image_name} (Image ID: {self.pk})")
    #         except Image.DoesNotExist:
    #             pass

    #     if image_changed and self.image:
    #         logger.info(f"[IMAGE SAVE] New image uploading (Image ID: {self.pk if not is_new else 'NEW'})")

    #     super().save(*args, **kwargs)

    #     if image_changed and self.image and hasattr(self.image, 'path'):
    #         try:
    #             original_image_name = self.image.name
    #             logger.info(f"[IMAGE SAVE] Uploaded file: {original_image_name}")
    #             logger.info(f"[IMAGE SAVE] Converting image to WebP: {self.image.path}")
                
    #             img = PilImage.open(self.image.path)
    #             if img.mode != "RGB":
    #                 img = img.convert("RGB")

    #             buffer = BytesIO()
    #             img.save(buffer, format="WEBP", quality=80)
    #             buffer.seek(0)

    #             webp_name = self.image.name.rsplit(".", 1)[0] + ".webp"
    #             logger.info(f"[IMAGE SAVE] WebP file name: {webp_name}")
                
    #             old_webp_name = None
    #             if old_image_name and old_image_name.lower().endswith('.webp'):
    #                 old_webp_name = old_image_name
    #                 logger.info(f"[IMAGE SAVE] Old WebP file: {old_webp_name}")
    #             elif old_image_name:
    #                 old_webp_name = old_image_name.rsplit(".", 1)[0] + ".webp"
    #                 logger.info(f"[IMAGE SAVE] Old WebP file (estimated): {old_webp_name}")
                
    #             self.image.save(webp_name, ContentFile(buffer.read()), save=False)
    #             buffer.close()
    #             logger.info(f"[IMAGE SAVE] WebP file created: {webp_name}")
                
    #             storage = default_storage
                
    #             if original_image_name and original_image_name != webp_name:
    #                 try:
    #                     logger.info(f"[IMAGE SAVE] Checking original file: {original_image_name}")
    #                     if storage.exists(original_image_name):
    #                         storage.delete(original_image_name)
    #                         logger.info(f"[IMAGE SAVE] Original file deleted: {original_image_name}")
    #                     else:
    #                         logger.warning(f"[IMAGE SAVE] Original file not found: {original_image_name}")
    #                 except Exception as e:
    #                     logger.error(f"[IMAGE SAVE] Error deleting original file: {e}")

    #             if old_webp_name and old_webp_name != webp_name:
    #                 try:
    #                     if storage.exists(old_webp_name):
    #                         storage.delete(old_webp_name)
    #                         logger.info(f"[IMAGE SAVE] Old WebP file deleted: {old_webp_name}")
    #                 except Exception as e:
    #                     logger.error(f"[IMAGE SAVE] Error deleting old WebP file: {e}")

    #             if old_image_name and old_image_name != webp_name and not old_image_name.lower().endswith('.webp'):
    #                 try:
    #                     if storage.exists(old_image_name):
    #                         storage.delete(old_image_name)
    #                         logger.info(f"[IMAGE SAVE] Old original file deleted: {old_image_name}")
    #                 except Exception as e:
    #                     logger.error(f"[IMAGE SAVE] Error deleting old original file: {e}")

    #             super().save(update_fields=['image'])
    #             logger.info(f"[IMAGE SAVE] Image successfully saved (Image ID: {self.pk})")
    #         except Exception as e:
    #             logger.error(f"[IMAGE SAVE] Error occurred: {e}")


    def delete(self, *args, **kwargs):
        image_id = self.pk
        logger.info(f"[IMAGE DELETE] Deleting image (Image ID: {image_id})")
        
        self.delete_files()
        
        super().delete(*args, **kwargs)
        
        logger.info(f"[IMAGE DELETE] Image successfully deleted (Image ID: {image_id})")