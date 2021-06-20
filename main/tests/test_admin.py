from decimal import Decimal
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from selenium.webdriver.chrome.webdriver import WebDriver
from main import models


class ProductImageAdminTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(executable_path=settings.CHROMEDRIVER)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_product_image_admin_list_page_displays_thumbnail_image_tag(self):
        user = User.objects.create(username='admin', is_superuser=True, is_active=True, is_staff=True)
        user.set_password('1234pass')
        user.save()
        product = models.Product(name='Product 1', price=Decimal('5.00'))
        product.save()
        with open('main/fixtures/the-cathedral-the-bazaar.jpg', 'rb') as f:
            product_image = models.ProductImage(product=product, image=ImageFile(f, 'tctb.jpg'))
            product_image.save()
        self.selenium.get('%s%s' % (self.live_server_url, '/admin'))
        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys(user.username)
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('1234pass')
        self.selenium.find_element_by_css_selector('input[type="submit"]').click()

        self.selenium.find_element_by_link_text('Product images').click()
        # import pdb; pdb.set_trace()
        product_image_thumbnail = self.\
            selenium.find_element_by_css_selector('th.field-thumbnail_tag > a > img')
        thumbnail_width = product_image_thumbnail.get_attribute('width')
        self.assertEqual(thumbnail_width, '70')
        thumbnail_src = product_image_thumbnail.get_attribute('src')
        self.assertEqual(thumbnail_src, self.live_server_url + product_image.thumbnail.url)

        product_image.image.delete(save=False)
        product_image.thumbnail.delete(save=False)
