from decimal import Decimal
from django.test import TestCase
from main import models


class TestModel(TestCase):
    def test_product_str_representation(self):
        p = models.Product.objects.create(
            name="The cathedral and the bazaar",
            price=Decimal("10.00")
        )
        self.assertEqual(str(p), p.name)

    def test_product_tag_str_representation(self):
        tag = models.ProductTag.objects.create(
            name='Fiction',
            slug='fiction'
        )
        self.assertEqual(str(tag), tag.name)

    def test_active_manager_works(self):
        models.Product.objects.create(
            name="The cathedral and the bazaar",
            price=Decimal("10.00")
        )
        models.Product.objects.create(
            name="Pride and Prejudice",
            price=Decimal("2.00")
        )
        models.Product.objects.create(
            name="A Tale of Two Citie",
            price=Decimal("2.00"),
            active=False
        )
        self.assertEqual(len(models.Product.objects.active()), 2)

    def test_product_tag_manager_works(self):
        tag1 = models.ProductTag.objects.create(
            name='Fiction',
            slug='fiction'
        )
        tag2 = models.ProductTag.objects.create(
            name='Romance',
            slug='romance'
        )
        self.assertEqual(models.ProductTag.objects.get_by_natural_key(tag1.slug), tag1)
        self.assertEqual(models.ProductTag.objects.get_by_natural_key(tag2.slug), tag2)
        self.assertNotEqual(models.ProductTag.objects.get_by_natural_key(tag2.slug), tag1)

    def test_product_tag_natural_key(self):
        tag1 = models.ProductTag.objects.create(
            name='Fiction',
            slug='fiction'
        )
        self.assertEqual(tag1.natural_key(), (tag1.slug,))
