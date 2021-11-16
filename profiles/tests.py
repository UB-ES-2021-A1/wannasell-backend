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

        # Create disabled user
        self.disabled_user = User.objects.create_user('disabled', 'disabled@disabled.com', 'disabled')
        self.disabled_user.is_active = False
        self.disabled_user.save()

        # Get and define user's profile attributes
        self.profile = Profile.objects.get(user=self.user)
        self.profile.bio = 'Test Bio'
        self.profile.address = 'Test Address'
        self.profile.save()

        # Add authorization to the requests headers
        self.client = APIClient()
        self.adminClient = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.adminClient.credentials(HTTP_AUTHORIZATION='Token ' + self.adminToken)

    def test_profile_get_info(self):
        request = self.client.get('/api/v1/profile/')
        assert request.data.get('bio') == 'Test Bio'
        assert request.data.get('address') == 'Test Address'

    def test_profile_get_info_disabled(self):
        request = self.client.get('/api/v1/profile/3/')
        assert request.status_code == 401

    def test_profile_admin_get_info_disabled(self):
        request = self.adminClient.get('/api/v1/profile/3/')
        assert request.status_code == 200

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
        data = {
            'bio': 'test2bio',
            'address': 'test2address'
        }
        request = self.adminClient.patch('/api/v1/profile/?username=testUser2', data, format='json')

        assert request.status_code == 200

        # Retrieve new Profile object
        profile = Profile.objects.get(user=self.user)
        assert profile.bio == 'test2bio'
        assert profile.address == 'test2address'

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
