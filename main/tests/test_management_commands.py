from decimal import Decimal
from io import StringIO
import tempfile
from django.test import TestCase, override_settings
from django.core.management import call_command
from main import models


class TestImport(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_import_data(self):
        out = StringIO()
        args = ["main/fixtures/product-sample.csv",
                "main/fixtures/product-sampleimages/"]

        # Create 1 product and 2 tags - that are already in the CSV file
        # to test the branch that involves `created`
        models.Product.objects.create(name='Siddhartha', price=Decimal('6.00'))
        models.ProductTag.objects.create(name='Programming', slug='programming')
        models.ProductTag.objects.create(name='Religion', slug='religion')

        call_command('import_data', *args, stdout=out)
        expected_out = ("Importing products\n"
                        "Products processed=3 (created=2)\n"
                        "Tags processed=6 (created=4)\n"
                        "Images created=2\n")
        self.assertEqual(out.getvalue(), expected_out)
        self.assertEqual(models.Product.objects.count(), 3)
        self.assertEqual(models.ProductTag.objects.count(), 6)
        self.assertEqual(models.ProductImage.objects.count(), 2)
