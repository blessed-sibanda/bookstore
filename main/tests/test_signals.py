import tempfile
from PIL import Image
from django.test import TestCase, override_settings
from django.core.files.images import ImageFile
# from django.conf import settings
from decimal import Decimal
from main import models


class TestSignal(TestCase):
    # @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_thumbnails_are_generated_on_save(self):
        product = models.Product(
            name="The cathedral and the bazaar",
            price=Decimal("10.00")
        )
        product.save()

        with open('main/fixtures/the-cathedral-the-bazaar.jpg', 'rb') as f:
            image = models.ProductImage(
                product=product,
                image=ImageFile(f, name='tctb.jpg')
            )
            with self.assertLogs('main', level='INFO') as cm:
                image.save()

        self.assertGreaterEqual(len(cm.output), 1)
        image.refresh_from_db()

        thumb = Image.open(image.thumbnail.url[1:])
        self.assertLessEqual(thumb.width, 300)
        self.assertLessEqual(thumb.height, 300)

        image.image.delete(save=False)
        image.thumbnail.delete(save=False)



