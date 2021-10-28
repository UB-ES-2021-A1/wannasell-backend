from django.test import TestCase
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from products.models import Product, Category, Image


# Create your tests here.
from products.serializers import ImageDataSerializer


class ProductsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.c = Category.objects.create(name='MO', grayscale_image='img.png', green_image='img.png')
        self.u = User.objects.create_user('testUser2', 'lennon@thebeatles.com', 'johnpassword')
        self.token = Token.objects.get_or_create(user=self.u)[0].__str__()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_get_products_succesfull(self):
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p.save()
        request = self.client.get('/api/v1/products/', format='json')
        self.assertEqual(request.status_code, 200)

    def test_get_empty_products(self):
        request = self.client.get('/api/v1/products/', format='json')
        self.assertEqual(request.status_code, 204)

    def test_get_products_by_category_fail(self):
        request = self.client.get("/api/v1/products/?category=MA", format='json')
        self.assertEqual(request.status_code, 500)

    def test_get_products_by_category_success(self):
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p.save()
        request = self.client.get("/api/v1/products/?category=MO", format='json')
        self.assertEqual(request.status_code, 200)

    def test_get_products_by_category_empty_success(self):
        request = self.client.get("/api/v1/products/?category=MO", format='json')
        self.assertEqual(request.status_code, 204)

    def test_get_category(self):
        request = self.client.get("/api/v1/products/categories/")
        self.assertEqual(request.status_code, 200)

    def test_post_product(self):
        data = {
            'title': 'Moto',
            'description': 'Una moto',
            'price': 12,
            'user': self.u,
            'category_name': 'MO'
        }
        request = self.client.post("/api/v1/products/", data)
        self.assertEqual(request.status_code, 200)

    def test_get_product_by_id(self):
        Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        request = self.client.get("/api/v1/products/?id=1", format='json')
        self.assertEqual(request.status_code, 200)

    def test_get_images_of_product(self):
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p.save()
        prod_id = (Product.objects.get(title='Title')).id
        Image.objects.create(product=p, image='fake1')
        Image.objects.create(product=p, image='fake2')

        request = self.client.get("/api/v1/products/images/?id=" + str(prod_id), format='json')

        images = request.data
        assert len(images) == 2
        self.assertEqual(request.status_code, 200)
