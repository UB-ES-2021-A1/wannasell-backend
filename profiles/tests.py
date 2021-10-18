from django.test import TestCase
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from profiles.models import Profile
# Create your tests here.
from profiles.serializers import ProfileDetailsSerializer


class ProfileTestCase(TestCase):
    def setUp(self):
        # Create User and Auth Token
        self.user = User.objects.create_user('testUser2', 'lennon@thebeatles.com', 'johnpassword')
        self.token = Token.objects.get_or_create(user=self.user)[0].__str__()

        # Get and define user's profile attributes
        self.profile = Profile.objects.get(user=self.user)
        self.profile.bio = 'Test Bio'
        self.profile.address = 'Test Address'
        # Need to add avatar
        self.profile.save()

        # Add authorization to the requests headers
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_profile_get_info(self):
        request = self.client.get('/api/v1/profile/', format='json')
        data = ProfileDetailsSerializer(request.data).data
        assert data.get('bio') == 'Test Bio'
        assert data.get('address') == 'Test Address'
        # Don't know how to test avatar


