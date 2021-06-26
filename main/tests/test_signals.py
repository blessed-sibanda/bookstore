import os
from PIL import Image
from django.test import TestCase
from django.core.files.images import ImageFile
from decimal import Decimal
from main import models


class TestSignal(TestCase):
    def setUp(self):
        self.product = models.Product(
            name="The cathedral and the bazaar",
            price=Decimal("10.00")
        )
        self.product.save()
        with open('main/fixtures/the-cathedral-the-bazaar.jpg', 'rb') as f:
            self.image = models.ProductImage(
                product=self.product,
                image=ImageFile(f, name='tctb.jpg')
            )
            with self.assertLogs('main', level='INFO') as cm:
                self.cm = cm
                self.image.save()

    def test_thumbnails_are_generated_on_save(self):
        self.assertGreaterEqual(len(self.cm.output), 1)
        self.image.refresh_from_db()

        thumbnail_url = self.image.thumbnail.url[1:]
        with Image.open(thumbnail_url) as thumb:
            self.assertLessEqual(thumb.width, 300)
            self.assertLessEqual(thumb.height, 300)

        self.image.image.delete(save=False)
        os.remove(thumbnail_url)
        self.image.thumbnail.delete(save=False)

    def test_deleting_productimage_deletes_image_and_thumbnail_files(self):
        image_url = self.image.image.url[1:]
        thumbnail_url = self.image.thumbnail.url[1:]
        self.assertTrue(os.path.exists(image_url))
        self.assertTrue(os.path.exists(thumbnail_url))
        self.image.delete()
        self.assertFalse(os.path.exists(image_url))
        self.assertFalse(os.path.exists(thumbnail_url))
