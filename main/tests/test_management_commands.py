import csv
from decimal import Decimal
from io import StringIO
import tempfile
from django.test import TestCase, override_settings
from django.core.management import call_command
from django.conf import settings
from main import models


class TestImport(TestCase):
    def setUp(self):
        self.out = StringIO()

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_import_data(self):
        args = ["main/fixtures/product-sample.csv",
                "main/fixtures/product-sampleimages/"]

        # Create 1 product and 2 tags - that are already in the CSV file
        # to test the branch that involves `created`
        models.Product.objects.create(name='Siddhartha', price=Decimal('6.00'))
        models.ProductTag.objects.create(name='Programming', slug='programming')
        models.ProductTag.objects.create(name='Religion', slug='religion')

        call_command('import_data', *args, stdout=self.out)
        expected_out = ("Importing products\n"
                        "Products processed=3 (created=2)\n"
                        "Tags processed=6 (created=4)\n"
                        "Images created=2\n")
        self.assertEqual(self.out.getvalue(), expected_out)
        self.assertEqual(models.Product.objects.count(), 3)
        self.assertEqual(models.ProductTag.objects.count(), 6)
        self.assertEqual(models.ProductImage.objects.count(), 2)

    def test_import_data_rejects_wrong_csv_file_path(self):
        args = ["main/fixtures/unknown.csv",
                "main/fixtures/product-sampleimages/"]

        call_command('import_data', *args, stdout=self.out)
        expected_out = ("Importing products\n"
                        f"The file: '{settings.BASE_DIR / args[0]}' does not exist\n")
        self.assertEqual(self.out.getvalue(), expected_out)
        self.assertEqual(models.Product.objects.count(), 0)
        self.assertEqual(models.ProductTag.objects.count(), 0)
        self.assertEqual(models.ProductImage.objects.count(), 0)

    def test_import_data_rejects_wrong_images_path(self):
        args = ["main/fixtures/product-sample.csv",
                "main/some/wrong/path"]

        call_command('import_data', *args, stdout=self.out)
        expected_out = ("Importing products\n"
                        f"The directory: '{settings.BASE_DIR / args[1]}' does not exist\n")
        self.assertEqual(self.out.getvalue(), expected_out)
        self.assertEqual(models.Product.objects.count(), 0)
        self.assertEqual(models.ProductTag.objects.count(), 0)
        self.assertEqual(models.ProductImage.objects.count(), 0)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_import_data_does_not_create_products_with_nonexistent_image(self):
        out = StringIO()
        args = ["main/fixtures/product-sample-with-nonexistent-image.csv",
                "main/fixtures/product-sampleimages/"]

        call_command('import_data', *args, stdout=out)
        product_name = 'The cathedral and the bazaar'
        image_path = 'wrong-image.jpg'
        expected_out = ("Importing products\n"
                        f"Could not create product '{product_name}' and its image: '{settings.BASE_DIR / args[1] / image_path}'\n"
                        f"The image: '{settings.BASE_DIR / args[1] / image_path}' does not exist\n"
                        "Products processed=2 (created=2)\n"
                        "Tags processed=4 (created=4)\n"
                        "Images created=2\n"
                        )

        self.assertEqual(out.getvalue(), expected_out)
        self.assertEqual(models.Product.objects.count(), 2)
        self.assertEqual(models.ProductTag.objects.count(), 4)
        self.assertEqual(models.ProductImage.objects.count(), 2)
