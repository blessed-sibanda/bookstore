import tempfile
from django.test import TestCase, override_settings
from django.core.files.images import ImageFile
from decimal import Decimal
from main import models


class TestSignal(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
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

        with open("main/fixtures/the-cathedral-the-bazaar.thumb.jpg", "rb") as f:
            expected_content = f.read()
            self.assertEqual(image.thumbnail.read(), expected_content)



