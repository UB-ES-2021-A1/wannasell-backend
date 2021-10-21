from django.test import TestCase
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from profiles.models import Profile
from profiles.serializers import ProfileDetailsSerializer


# TODO Add avatar testing cases (PUT profile missing)
class ProfileTestCase(TestCase):
    def setUp(self):
        # Create User and Auth Token
        self.user = User.objects.create_user('testUser2', 'lennon@thebeatles.com', 'johnpassword')
        self.admin_user = User.objects.create_superuser('testAdmin', 'admin@admin.es', 'testAdminPassword')
        self.token = Token.objects.get_or_create(user=self.user)[0].__str__()
        self.adminToken = Token.objects.get_or_create(user=self.admin_user)[0].__str__()

        # Get and define user's profile attributes
        self.profile = Profile.objects.get(user=self.user)
        self.profile.bio = 'Test Bio'
        self.profile.address = 'Test Address'
        self.profile.save()

        # Add authorization to the requests headers
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_profile_get_info(self):
        request = self.client.get('/api/v1/profile/')
        data = ProfileDetailsSerializer(request.data).data
        assert data.get('bio') == 'Test Bio'
        assert data.get('address') == 'Test Address'

    def test_profile_patch_info(self):
        data = {
            'bio': 'test2bio',
            'address': 'test2address'
        }
        request = self.client.patch('/api/v1/profile/', data, format='json')

        # Retrieve new Profile object
        profile = Profile.objects.get(user=self.user)
        assert profile.bio == 'test2bio'
        assert profile.address == 'test2address'

    def test_profile_patch_other_info_no_perms(self):
        data = {
            'bio': 'test2bio',
            'address': 'test2address'
        }
        request = self.client.patch('/api/v1/profile/?username=testAdmin', data, format='json')

        assert request.status_code == 401

        # Retrieve new Profile object
        profile = Profile.objects.get(user=self.admin_user)
        assert profile.bio != 'test2bio'
        assert profile.address != 'test2address'

    def test_profile_patch_other_info(self):
        # Set Admin token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.adminToken)

        data = {
            'bio': 'test2bio',
            'address': 'test2address'
        }
        request = self.client.patch('/api/v1/profile/?username=testAdmin', data, format='json')

        assert request.status_code == 401

        # Retrieve new Profile object
        profile = Profile.objects.get(user=self.user)
        assert profile.bio == 'test2bio'
        assert profile.address == 'test2address'
