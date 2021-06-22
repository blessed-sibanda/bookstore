from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.core import mail
from main import forms, models


class TestPage(TestCase):
    def test_home_page_works(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'BookStore')

    def test_about_us_page_works(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
        self.assertContains(response, 'BookStore')

    def test_contact_us_page_works(self):
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertIsInstance(response.context['form'], forms.ContactForm)

    def test_contact_us_page_sends_email_upon_form_submission(self):
        response = self.client.post(reverse('contact_us'),
                                    data={'name': 'Blessed',
                                          'message': 'Hello there'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)

    def test_products_page_returns_active(self):
        models.Product.objects.create(
            name='The cathedral and the bazaar',
            slug='cathedral-bazaar',
            price=Decimal('10.00'),
        )
        models.Product.objects.create(
            name='A Tale of Two Cities',
            slug='tale-two-cities',
            price=Decimal('2.00'),
            active=False
        )
        response = self.client.get(
            reverse('products', kwargs={'tag': 'all'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'BookStore')
        product_list = models.Product.objects.active().order_by('name')
        self.assertEqual(
            list(response.context['products']),
            list(product_list)
        )

    def test_products_page_filters_by_tags_and_active(self):
        cb = models.Product.objects.create(
            name='The cathedral and the bazaar',
            slug='cathedral-bazaar',
            price=Decimal('10.00'),
        )
        cb.tags.create(name='Open source', slug='opensource')
        models.Product.objects.create(
            name='Microsoft Windows Guide',
            slug='microsoft-windows-guide',
            price=Decimal('12.00'),
        )
        response = self.client.get(
            reverse('products', kwargs={'tag': 'opensource'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'BookStore')
        product_list = models.Product.objects.active(). \
            filter(tags__slug='opensource').order_by('name')
        self.assertEqual(
            list(response.context['products']),
            list(product_list)
        )

    def test_products_page_paginates_products_by_five(self):
        for i in range(12):
            models.Product.objects.create(name=f'Product {i}', slug=f'product-{1}', price=Decimal('5.00'))

        response = self.client.get(
            reverse('products', kwargs={'tag': 'all'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/product_list.html')
        self.assertTemplateUsed(response, 'main/_pagination.html')
        product_list = models.Product.objects.active().order_by("name")[:5]
        self.assertEqual(
            list(response.context['products']),
            list(product_list)
        )

        response = self.client.get(
            reverse('products', kwargs={'tag': 'all'}) + '?page=2'
        )
        self.assertEqual(response.status_code, 200)
        product_list = models.Product.objects.active().order_by("name")[5:10]
        self.assertEqual(
            list(response.context['products']),
            list(product_list)
        )

    def test_product_detail_page_works(self):
        p = models.Product.objects.create(
            name='The cathedral and the bazaar',
            slug='cathedral-bazaar',
            price=Decimal('10.00'),
        )
        response = self.client.get(reverse('product', kwargs={'slug': p.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, p.name)
        self.assertContains(response, str(p.price))
