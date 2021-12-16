from django.db.models import Q, Avg
from django.test import TestCase
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

import profiles.models
from favorites.models import Favorites
from products.models import Product, Category
from profiles.models import Profile


# TODO Add avatar testing cases (PUT profile missing)
from reviews.models import Review


class ProfileTestCase(TestCase):
    def setUp(self):
        # Create User and Auth Token
        self.user = User.objects.create_user('testUser2', 'lennon@thebeatles.com', 'johnpassword')
        self.admin_user = User.objects.create_superuser('testAdmin', 'admin@admin.es', 'testAdminPassword')
        self.token = Token.objects.get_or_create(user=self.user)[0].__str__()
        self.adminToken = Token.objects.get_or_create(user=self.admin_user)[0].__str__()

        # Create disabled user
        self.disabled_user = User.objects.create_user('disabled', 'disabled@disabled.com', 'disabled')
        self.disabled_user.is_active = False
        self.disabled_user.save()

        # Get and define user's profile attributes
        self.profile = Profile.objects.get(user=self.user)
        self.profile.bio = 'Test Bio'
        self.profile.address = 'Test Address'
        self.profile.location = 'Test Location'
        self.profile.phone = '659448329'
        self.profile.countryCode = 'ES'
        self.profile.countryCallingCode = '34'
        self.profile.save()

        # Add authorization to the requests headers
        self.client = APIClient()
        self.adminClient = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.adminClient.credentials(HTTP_AUTHORIZATION='Token ' + self.adminToken)

        self.user2 = User.objects.create_user('testUserPepe', 'lennon3@thebeatles.com', 'johnpassword')

    def test_profile_get_info(self):
        request = self.client.get('/api/v1/profile/')
        assert request.data.get('bio') == 'Test Bio'
        assert request.data.get('address') == 'Test Address'
        assert request.data.get('location') == 'Test Location'

    def test_profile_get_info_disabled(self):
        request = self.client.get('/api/v1/profile/3/')
        assert request.status_code == 401

    def test_profile_admin_get_info_disabled(self):
        request = self.adminClient.get('/api/v1/profile/3/')
        assert request.status_code == 200

    def test_profile_patch_info(self):
        data = {
            'bio': 'test2bio',
            'address': 'test2address',
            'location': 'test2location',
            'phone': '659448329',
            'countryCallingCode': '34',
            'countryCode': 'ES'

        }
        request = self.client.patch('/api/v1/profile/', data, format='json')

        # Retrieve new Profile object
        profile = Profile.objects.get(user=self.user)
        assert profile.bio == 'test2bio'
        assert profile.address == 'test2address'
        assert profile.location == 'test2location'
        assert profile.phone == '659448329'
        assert profile.countryCallingCode == '34'
        assert profile.countryCode == 'ES'

    def test_profile_patch_other_info_no_perms(self):
        data = {
            'bio': 'test2bio',
            'address': 'test2address',
            'location': 'test2location'
        }
        request = self.client.patch('/api/v1/profile/?username=testAdmin', data, format='json')

        assert request.status_code == 401

        # Retrieve new Profile object
        profile = Profile.objects.get(user=self.admin_user)
        assert profile.bio != 'test2bio'
        assert profile.address != 'test2address'
        assert profile.location != 'test2location'

    def test_profile_patch_other_info(self):
        data = {
            'bio': 'test2bio',
            'address': 'test2address',
            'location': 'test2location'
        }
        request = self.adminClient.patch('/api/v1/profile/?username=testUser2', data, format='json')

        assert request.status_code == 200

        # Retrieve new Profile object
        profile = Profile.objects.get(user=self.user)
        assert profile.bio == 'test2bio'
        assert profile.address == 'test2address'
        assert profile.location == 'test2location'

    def test_delete_profile(self):
        request = self.client.delete('/api/v1/profile/')

        assert request.status_code == 200
        assert User.objects.get(username='testUser2').is_active == 0

    def test_admin_delete_other_profile(self):
        request = self.adminClient.delete('/api/v1/profile/1/')

        assert request.status_code == 200
        assert User.objects.get(username='testUser2').is_active == 0

    def test_no_admin_delete_other_profile(self):
        request = self.client.delete('/api/v1/profile/2/')

        assert request.status_code == 401
        assert User.objects.get(username='testUser2').is_active == 1

    def test_profile__str__(self):
        user = Profile.objects.get(user__username='testUser2')
        assert str(user) == 'testUser2'

    def test_get_user_directory_path(self):
        profile = Profile.objects.get(user__username='testUser2')
        path = profiles.models.user_directory_path(profile, 'test')
        assert path == 'images/avatars/1/test'

    def test_get_username_param(self):
        request = self.client.get('/api/v1/profile/?username=testUser2')
        assert request.data.get('bio') == 'Test Bio'
        assert request.data.get('address') == 'Test Address'
        assert request.data.get('location') == 'Test Location'

    def test_get_username_param_exc(self):
        request = self.client.get('/api/v1/profile/?username=testUser3')
        assert request.status_code == 500

    def test_user_get_disabled_username(self):
        profile = Profile.objects.get(user__username='testUser2')
        user = User.objects.get(username='testUser2')
        user.is_active = 0
        user.save()
        request = self.client.get('/api/v1/profile/?username=testUser2')
        assert request.status_code == 401

    def test_admin_get_disabled_username(self):
        profile = Profile.objects.get(user__username='testUser2')
        user = User.objects.get(username='testUser2')
        user.is_active = 0
        user.save()
        request = self.adminClient.get('/api/v1/profile/?username=testUser2')
        assert request.status_code == 200

    def test_admin_patch_wrong_user(self):
        request = self.adminClient.patch('/api/v1/profile/?username=testUser3')
        assert request.status_code == 500

    def test_admin_patch_bad_req(self):
        data = {
            'location': 'testtesttesttesttesttesttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessfttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessfttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessfttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessftttessfttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttsftttessftttessftttessftttessftttessftttessftttesftttessftttessftttessftttessftttessftttessftttesftttessftttessftttessftttessftttessftttessfttte',
        }
        request = self.adminClient.patch('/api/v1/profile/?juan=testUser2', data)
        assert request.status_code == 400

    def test_profile_no_exists(self):
        request = self.adminClient.get('/api/v1/profile/200/')
        assert request.status_code == 500

    def test_self_delete(self):
        request = self.client.delete('/api/v1/profile/')
        assert request.status_code == 200

    def test_products_sold(self):
        cat = Category.objects.create(name='MO', grayscale_image='img.png', green_image='img.png')
        prod1 = Product.objects.create(price=5, category=cat, seller=self.user)
        prod2 = Product.objects.create(price=5, category=cat, sold=True, seller=self.user)
        prod3 = Product.objects.create(price=5, category=cat, sold=True, seller=self.user)
        prod1.save()
        prod2.save()
        prod3.save()
        request = self.client.get('/api/v1/profile/')
        assert request.data['n_sold_products'] == 2

    def test_products_selling(self):
        cat = Category.objects.create(name='MO', grayscale_image='img.png', green_image='img.png')
        prod1 = Product.objects.create(price=5, category=cat, seller=self.user)
        prod2 = Product.objects.create(price=5, category=cat, sold=True, seller=self.user)
        prod3 = Product.objects.create(price=5, category=cat, sold=True, seller=self.user)
        prod1.save()
        prod2.save()
        prod3.save()
        request = self.client.get('/api/v1/profile/')
        assert request.data['n_selling_products'] == 1

    def test_products_favorited(self):
        cat = Category.objects.create(name='MO', grayscale_image='img.png', green_image='img.png')
        prod1 = Product.objects.create(price=5, category=cat, seller=self.user)
        prod2 = Product.objects.create(price=5, category=cat, sold=True, seller=self.user)
        prod3 = Product.objects.create(price=5, category=cat, sold=True, seller=self.user)
        fav1 = Favorites.objects.create(product=prod1, user=self.user)
        fav2 = Favorites.objects.create(product=prod2, user=self.user)
        prod1.save()
        prod2.save()
        prod3.save()
        fav1.save()
        fav2.save()
        request = self.client.get('/api/v1/profile/')
        assert request.data['n_favorite_products'] == 2

    def test_user_review_mean(self):
        cat = Category.objects.create(name='MO', grayscale_image='img.png', green_image='img.png')
        prod1 = Product.objects.create(price=5, category=cat, seller=self.user)
        prod2 = Product.objects.create(price=5, category=cat, sold=True, seller=self.user)
        prod3 = Product.objects.create(price=5, category=cat, sold=True, seller=self.user)
        review1 = Review.objects.create(reviewer=self.user, seller=self.user, val=3, check=True)
        review2 = Review.objects.create(reviewer=self.user2, seller=self.user, val=4, check=True)
        prod1.save()
        prod2.save()
        prod3.save()
        review1.save()
        review2.save()
        request = self.client.get('/api/v1/profile/')
        assert request.data['review_mean'] == 3.5



