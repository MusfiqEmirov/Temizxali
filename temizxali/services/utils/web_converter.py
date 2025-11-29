import threading
from PIL import Image as PilImage
from io import BytesIO
from django.core.files.base import ContentFile


def convert_to_webp(instance):
    from services.models.image_models import Image
    try:
        path = instance.image.path
        img = PilImage.open(path)

        if img.mode != "RGB":
            img = img.convert("RGB")

        # Resize (opsional)
        max_width = 1920
        if img.width > max_width:
            ratio = max_width / img.width
            height = int(img.height * ratio)
            img = img.resize((max_width, height), PilImage.LANCZOS)

        # WebP output
        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=70, optimize=True)
        buffer.seek(0)

        webp_name = instance.image.name.rsplit(".", 1)[0] + ".webp"
        
        try:
            if instance.image.storage.exists(webp_name):
                instance.image.storage.delete(webp_name)
        except Exception:
            pass

        instance.image.storage.save(webp_name, ContentFile(buffer.read()))

        buffer.close()

    except Exception as e:
        print("WebP convert error:", e)


def run_async(func, *args):
    t = threading.Thread(target=func, args=args)
    t.daemon = True
    t.start()

