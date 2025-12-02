import threading
from PIL import Image as PilImage
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import close_old_connections
from django.core.files.storage import default_storage
import logging

logger = logging.getLogger(__name__)

_thread_semaphore = threading.Semaphore(3)


def convert_to_webp(image_id, image_path, image_name):
    close_old_connections()
    
    try:
        img = PilImage.open(image_path)

        if img.mode != "RGB":
            img = img.convert("RGB")

        max_width = 1920
        if img.width > max_width:
            ratio = max_width / img.width
            height = int(img.height * ratio)
            img = img.resize((max_width, height), PilImage.LANCZOS)

        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=70, optimize=True)
        buffer.seek(0)

        webp_name = image_name.rsplit(".", 1)[0] + ".webp"
        storage = default_storage
        
        try:
            if storage.exists(webp_name):
                storage.delete(webp_name)
        except Exception as e:
            logger.warning(f"Köhnə WebP faylını silməkdə xəta: {e}")

        storage.save(webp_name, ContentFile(buffer.read()))
        buffer.close()
        
        logger.info(f"WebP çevirmə uğurla tamamlandı: {webp_name}")

    except Exception as e:
        logger.error(f"WebP convert error (Image ID: {image_id}): {e}", exc_info=True)
    finally:
        close_old_connections()


def _convert_to_webp_wrapper(image_id, image_path, image_name):
    _thread_semaphore.acquire()
    try:
        convert_to_webp(image_id, image_path, image_name)
    finally:
        _thread_semaphore.release()


def run_async(instance):
    try:
        image_id = instance.pk
        image_path = instance.image.path
        image_name = instance.image.name
        
        t = threading.Thread(
            target=_convert_to_webp_wrapper,
            args=(image_id, image_path, image_name),
            daemon=True
        )
        t.start()
    except Exception as e:
        logger.error(f"Thread yaratmada xəta (Image ID: {instance.pk if hasattr(instance, 'pk') else 'unknown'}): {e}", exc_info=True)

