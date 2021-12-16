import tempfile

from django.test import TestCase
import PIL
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from favorites.models import Favorites
from products.models import Product, Category, Image


# Create your tests here.
from profiles.models import Profile


class IntegrationTests(TestCase):
    def setUp(self):
        # Create User and Auth Token
        self.u = User.objects.create_user('testUser2', 'lennon@thebeatles.com', 'johnpassword')
        self.token = Token.objects.get_or_create(user=self.u)[0].__str__()

        # Create client
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Create category and product
        self.c = Category.objects.create(name='MO', grayscale_image='img.png', green_image='img.png')
        self.p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)

        # Get and define user's profile attributes
        self.profile = Profile.objects.get(user=self.u)
        self.profile.bio = 'Test Bio'
        self.profile.address = 'Test Address'
        self.profile.location = 'Test Location'
        self.profile.save()

    def test_upload_and_modify_product(self):

        data = {
            'title': 'Moto',
            'description': 'Una moto',
            'price': 12,
            'user': self.u,
            'category_name': 'MO'
        }
        post_request = self.client.post("/api/v1/products/", data)

        assert post_request.status_code == 200

        new_data = {
            'title': 'New moto',
            'description': 'New description',
            'price': 2,
            'user': self.u,
            'category_name': 'CO'
        }

        Category.objects.create(name='CO', grayscale_image='img.png', green_image='img.png')
        url = "/api/v1/products/?id=" + str(post_request.data['id'])
        patch_request = self.client.patch(url, new_data)

        assert patch_request.status_code == 200
        assert patch_request.data['title'] == 'New moto'
        assert patch_request.data['description'] == 'New description'
        assert patch_request.data['price'] == '2.00'
        assert patch_request.data['category_name'] == 'CO'

    def test_add_and_get_favorite_products(self):

        other_user = User.objects.create_user('otherUser', 'lennon@other.com', 'otherpassword')

        fav_product = Product.objects.create(title='Other Title', description='Description', price=1, seller=other_user, category=self.c)
        other_fav_product = Product.objects.create(title='Other Title 2', description='Description 2', price=1, seller=other_user, category=self.c)

        request_add_fav = self.client.post('/api/v1/favorites/{0}/'.format(fav_product.id), format='json')
        request_add_fav_2 = self.client.post('/api/v1/favorites/{0}/'.format(other_fav_product.id), format='json')

        assert request_add_fav.status_code == 200
        assert request_add_fav_2.status_code == 200

        request_get_favs = self.client.get('/api/v1/favorites/', format='json')

        assert request_get_favs.status_code == 200
        assert len(request_get_favs.data) == 2

    def test_publish_and_get_seller_products(self):

        data = {
            'title': 'Moto',
            'description': 'Una moto',
            'price': 12,
            'user': self.u,
            'category_name': 'MO'
        }
        self.client.post("/api/v1/products/", data)

        data = {
            'title': 'Moto 2',
            'description': 'Una moto 2',
            'price': 120,
            'user': self.u,
            'category_name': 'MO'
        }

        self.client.post("/api/v1/products/", data)

        other_user = User.objects.create_user('otherUser', 'lennon@other.com', 'otherpassword')
        Product.objects.create(title='Other Title', description='Description', price=1, seller=other_user,
                                         category=self.c)

        request = self.client.get("/api/v1/products/?seller={0}".format(self.u.username), format='json')

        self.assertEqual(request.status_code, 200)
        assert len(request.data) == 3

