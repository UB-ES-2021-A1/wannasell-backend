import tempfile

from django.test import TestCase
import PIL
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from contact.models import Contact
from products.models import Product, Category

# Create your tests here.


class ProductsTestCase(TestCase):
    def setUp(self):
        self.apiClient = APIClient()
        self.category = Category.objects.create(name='MO', grayscale_image='img.png', green_image='img.png')
        self.buyer = User.objects.create_user('testUser2', 'lennon@thebeatles.com', 'johnpassword')
        self.seller = User.objects.create_user('testUser3', 'seconduser@thebeatles.com', 'johnpassword')
        self.token = Token.objects.get_or_create(user=self.buyer)[0].__str__()
        self.apiClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.product = Product.objects.create(title='Test', description='test2', price=15, seller=self.seller,
                                              category=self.category)
        self.product.save()

    def test_contact_post(self):
        data = {
            'seller': 'testUser3',
            'product_id': self.product.id
        }
        request = self.apiClient.post('/api/v1/contact/', data=data)
        contact = Contact.objects.get(id=1)
        assert contact.buyer == self.buyer
        assert contact.seller == self.seller
        assert contact.product == self.product

    def test_contact_post_already_exists(self):
        data = {
            'seller': 'testUser3',
            'product_id': self.product.id
        }
        request = self.apiClient.post('/api/v1/contact/', data=data)
        contact = Contact.objects.get(id=1)
        assert contact.buyer == self.buyer
        assert contact.seller == self.seller
        assert contact.product == self.product
        request = self.apiClient.post('/api/v1/contact/', data=data)
        assert request.status_code == 500

    def test_get_contact(self):
        self.test_contact_post()
        request = self.apiClient.get('/api/v1/contact/')
        assert request.data[0]['buyer'] == self.buyer.id
        assert request.data[0]['seller'] == self.seller.id
        assert request.data[0]['product']['title'] == self.product.title

    def test_delete_contact(self):
        data = {
            'product_id': self.product.id
        }
        self.test_contact_post()
        request = self.apiClient.delete('/api/v1/contact/', data=data)
        assert len(Contact.objects.all()) == 0
