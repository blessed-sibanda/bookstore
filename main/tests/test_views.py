from django.test import TestCase
from django.urls import reverse
from django.core import mail
from main import forms


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