from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from favorites.models import Favorites
from products.models import Product, Category


# Create your tests here.


class FavoritesTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        c = Category.objects.create(name='MO', grayscale_image='img.png', green_image='img.png')
        self.u = User.objects.create_user('testUser2', 'lennon@thebeatles.com', 'johnpassword')
        us = User.objects.create_user('test', 'lon@ts.com', 'johnpassword')
        self.p = Product.objects.create(title='Title', description='Description', price=1, seller=us, category=c)
        self.token = Token.objects.get_or_create(user=self.u)[0].__str__()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_add_fav(self):
        request = self.client.post('/api/v1/favorites/{0}/'.format(self.p.id), format='json')
        assert request.status_code == 200
        assert len(Favorites.objects.filter(user=self.u)) == 1
        assert len(Favorites.objects.filter(product=self.p)) == 1

    def test_add_fav_already_added(self):
        f = Favorites.objects.create(user=self.u, product=self.p)
        request = self.client.post('/api/v1/favorites/{0}/'.format(self.p.id), format='json')
        assert request.status_code == 418
        assert request.data == 'Already exists'

    def test_add_fav_without_id(self):
        request = self.client.post('/api/v1/favorites/', format='json')
        assert request.status_code == 404
        assert len(Favorites.objects.filter(user=self.u)) == 0
        assert len(Favorites.objects.filter(product=self.p)) == 0

    def test_add_fav_unexistent_product(self):
        request = self.client.post('/api/v1/favorites/1234567/', format='json')
        assert request.status_code == 404
        assert len(Favorites.objects.filter(user=self.u)) == 0
        assert len(Favorites.objects.filter(product=self.p)) == 0

    def test_delete_fav(self):
        request = self.client.delete('/api/v1/favorites/{0}/'.format(self.p.id), format='json')
        assert request.status_code == 200
        assert len(Favorites.objects.filter(user=self.u)) == 0
        assert len(Favorites.objects.filter(product=self.p)) == 0

    def test_delete_fav_unexistent_product(self):
        request = self.client.delete('/api/v1/favorites/12345678/', format='json')
        assert request.status_code == 404
        assert len(Favorites.objects.filter(user=self.u)) == 0
        assert len(Favorites.objects.filter(product=self.p)) == 0

    def test_delete_fav_no_id(self):
        request = self.client.delete('/api/v1/favorites/', format='json')
        assert request.status_code == 404
        assert len(Favorites.objects.filter(user=self.u)) == 0
        assert len(Favorites.objects.filter(product=self.p)) == 0

    def test_get_fav_products(self):
        Favorites.objects.create(user=self.u, product=self.p)
        request = self.client.get('/api/v1/favorites/', format='json')
        assert request.status_code == 200
        assert len(request.data) == 1
