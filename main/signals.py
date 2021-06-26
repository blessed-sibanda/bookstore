import logging
import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from main.models import ProductImage

THUMBNAIL_SIZE = (300, 300)  # (width, height)
logger = logging.getLogger(__name__)


@receiver(pre_save, sender=ProductImage)
def generate_thumbnail(sender, instance, **kwargs):
    image = Image.open(instance.image)

    logger.info(
        "Generating thumbnail for product %d",
        instance.product.id
    )
    image = image.convert("RGB")
    image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
    temp_thumb = BytesIO()
    image.save(temp_thumb, 'JPEG')
    temp_thumb.seek(0)

    # set save=False, otherwise it will run in an infinite loop
    instance.thumbnail.save(
        instance.image.name,
        ContentFile(temp_thumb.read()),
        save=False
    )
    temp_thumb.close()


@receiver(pre_delete, sender=ProductImage)
def delete_image_and_thumbnail(sender, instance, **kwargs):
    image_url_path = instance.image.url[1:]
    if os.path.exists(image_url_path):
        os.remove(image_url_path)

    thumbnail_url_path = instance.thumbnail.url[1:]
    if os.path.exists(thumbnail_url_path):
        os.remove(thumbnail_url_path)
