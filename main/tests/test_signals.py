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
        self.image_url = self.image.image.url[1:]
        self.thumbnail_url = self.image.thumbnail.url[1:]

    def test_thumbnails_are_generated_on_save(self):
        self.assertGreaterEqual(len(self.cm.output), 1)
        self.image.refresh_from_db()

        with Image.open(self.thumbnail_url) as thumb:
            self.assertLessEqual(thumb.width, 300)
            self.assertLessEqual(thumb.height, 300)

        self.image.image.delete(save=False)
        os.remove(self.thumbnail_url)
        self.image.thumbnail.delete(save=False)

    def test_deleting_productimage_deletes_image_and_thumbnail_files(self):
        self.assertTrue(os.path.exists(self.image_url))
        self.assertTrue(os.path.exists(self.thumbnail_url))
        self.image.delete()
        self.assertFalse(os.path.exists(self.image_url))
        self.assertFalse(os.path.exists(self.thumbnail_url))

    def test_productimage_deletion_happens_even_if_image_and_thumbnail_have_been_removed(self):
        os.remove(self.image_url)
        os.remove(self.thumbnail_url)
        self.assertIsNotNone(self.image.id)
        self.image.delete()
        self.assertIsNone(self.image.id)
