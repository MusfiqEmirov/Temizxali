import subprocess
import os
from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.files import File
from django.core.files.storage import default_storage
from tempfile import NamedTemporaryFile
import logging

from services.utils import SluggedModel, LANGUAGES, MEASURE_TYPE_CHOICES

logger = logging.getLogger(__name__)


class Service(models.Model):
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Qiymət'
    )
    vip_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='VIP Qiymət'
    )
    premium_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Premium Qiymət',
    )
    video = models.FileField(
        upload_to='videos/',  
        null=True,
        blank=True,
        verbose_name='Video'
    )
    url = models.URLField(
        null=True,
        blank=True,
        verbose_name='Url'
    )
    is_vip = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Vip'
    )
    is_premium = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Premium'
    )
    measure_type = models.CharField(
        max_length=10, 
        choices=MEASURE_TYPE_CHOICES, 
        verbose_name='Ölçü Növü'
    )
    delivery = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Çatdırılma'
    )
    is_active = models.BooleanField(
        default=True,
        null=True,
        blank=True,
        verbose_name='Servis aktivliyi'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Servis yaradılma tarixi'
    )

    class Meta:
        verbose_name = 'Servis'
        verbose_name_plural = 'Servislər'
    
    def __str__(self):
        translation = self.translations.first()
        if translation:
            return translation.name
        return f'Service #{self.id}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        update_fields = kwargs.get('update_fields', [])
        video_changed = is_new or 'video' in update_fields or not update_fields

        old_video_name = None
        if not is_new and self.pk and video_changed:
            try:
                old_instance = Service.objects.get(pk=self.pk)
                if old_instance.video:
                    old_video_name = old_instance.video.name
                    logger.info(f"[SERVICE SAVE] Old video found: {old_video_name} (Service ID: {self.pk})")
            except Service.DoesNotExist:
                pass

        if video_changed:
            if self.video:
                logger.info(f"[SERVICE SAVE] New video uploading (Service ID: {self.pk if not is_new else 'NEW'})")
            elif old_video_name:
                logger.info(f"[SERVICE SAVE] Video being removed (Service ID: {self.pk})")

        super().save(*args, **kwargs)

        if video_changed:
            try:
                storage = default_storage

                if self.video:
                    current_video_name = self.video.name
                    logger.info(f"[SERVICE SAVE] Uploaded video: {current_video_name}")
                    logger.info(f"[SERVICE SAVE] Video path: {self.video.path if hasattr(self.video, 'path') else 'N/A'}")

                    if old_video_name and old_video_name != current_video_name:
                        try:
                            logger.info(f"[SERVICE SAVE] Checking old video: {old_video_name}")
                            logger.info(f"[SERVICE SAVE] Storage exists check for: {old_video_name}")
                            exists = storage.exists(old_video_name)
                            logger.info(f"[SERVICE SAVE] File exists: {exists}")
                            if exists:
                                storage.delete(old_video_name)
                                logger.info(f"[SERVICE SAVE] ✓ Old video deleted: {old_video_name}")
                            else:
                                logger.warning(f"[SERVICE SAVE] ✗ Old video not found: {old_video_name}")
                        except Exception as e:
                            logger.error(f"[SERVICE SAVE] Error deleting old video: {e}", exc_info=True)
                elif old_video_name:
                    try:
                        logger.info(f"[SERVICE SAVE] Video removed, deleting old file: {old_video_name}")
                        logger.info(f"[SERVICE SAVE] Storage exists check for: {old_video_name}")
                        exists = storage.exists(old_video_name)
                        logger.info(f"[SERVICE SAVE] File exists: {exists}")
                        if exists:
                            storage.delete(old_video_name)
                            logger.info(f"[SERVICE SAVE] ✓ Old video deleted: {old_video_name}")
                        else:
                            logger.warning(f"[SERVICE SAVE] ✗ Old video not found: {old_video_name}")
                    except Exception as e:
                        logger.error(f"[SERVICE SAVE] Error deleting old video: {e}", exc_info=True)

                logger.info(f"[SERVICE SAVE] Service successfully saved (Service ID: {self.pk})")
            except Exception as e:
                logger.error(f"[SERVICE SAVE] Error occurred: {e}")

    def delete(self, *args, **kwargs):
        service_id = self.pk
        logger.info(f"[SERVICE DELETE] Deleting service (Service ID: {service_id})")

        video_name = None
        if self.video:
            video_name = self.video.name
            logger.info(f"[SERVICE DELETE] Video file to delete: {video_name}")

        super().delete(*args, **kwargs)

        if video_name:
            try:
                logger.info(f"[SERVICE DELETE] Deleting video file from disk: {video_name}")
                storage = default_storage
                logger.info(f"[SERVICE DELETE] Storage exists check for: {video_name}")
                exists = storage.exists(video_name)
                logger.info(f"[SERVICE DELETE] File exists: {exists}")
                if exists:
                    storage.delete(video_name)
                    logger.info(f"[SERVICE DELETE] ✓ Video file deleted: {video_name}")
                else:
                    logger.warning(f"[SERVICE DELETE] ✗ Video file not found: {video_name}")
            except Exception as e:
                logger.error(f"[SERVICE DELETE] Error deleting video file: {e}", exc_info=True)

        logger.info(f"[SERVICE DELETE] Service successfully deleted (Service ID: {service_id})")


class ServiceVariant(models.Model):
    service = models.ForeignKey(
        Service,
        related_name='variants',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Servis üçün növlər'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Qiymət'
    )

    vip_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True, 
        blank=True,
        verbose_name='VIP Qiymət '
    )

    premium_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True, 
        blank=True,
        verbose_name='Premium Qiymət'
    )

    class Meta:
        verbose_name = 'Servis növü'
        verbose_name_plural = 'Servis növləri'

    def __str__(self):
        return f'{self.translations.name} — {self.service.translations.name}'


class ServiceTranslation(SluggedModel):
    service = models.ForeignKey(
        Service,
        related_name='translations',
        on_delete=models.CASCADE, 
        verbose_name='Servis',
    )
    languages = models.CharField(
        max_length=12,
        choices=LANGUAGES,
    )
    name = models.CharField(
        max_length=250,
        verbose_name='Ad'
    )
    description = models.TextField(
        validators=[MaxLengthValidator(4000)],
        verbose_name='Servis haqqında'
    )

    class Meta:
        verbose_name = 'Servis tərcüməsi'
        verbose_name_plural = 'Servis tərcümələri'
    
    def get_slug_source(self) -> str:
        return self.name

    def __str__(self):
        return f'{self.name}'


class ServiceVariantTranslation(models.Model):
    variant = models.ForeignKey(
        ServiceVariant,
        related_name='translations',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Növ'
    )
    languages = models.CharField(
        max_length=12,
        choices=LANGUAGES,
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Növ adı'
    )

    class Meta:
        verbose_name = 'Növ ad tərcüməsi'
        verbose_name_plural = 'Növ ad tərcümələri'

    def __str__(self):
        return f'{self.name}'

    

