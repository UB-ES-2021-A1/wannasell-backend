from django.test import TestCase
from rest_framework.authtoken.admin import User
from rest_framework.test import APIClient

from profiles.models import Profile


class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        User.objects.create_user('testUser2', 'lennon@thebeatles.com', 'johnpassword')

    def test_password_validation(self):
        data = {
            "username": "testUser",
            "email": "testUser@gmail.com",
            "password1": "12",
            "password2": "12"
        }
        request = self.client.post('/api/v1/auth/register/', data, format='json')
        self.assertEqual(request.status_code, 400)

    def test_register_user(self):
        data = {
            "username": "testUser",
            "email": "testUser@gmail.com",
            "password1": "testUserPassword123",
            "password2": "testUserPassword123"
        }
        request = self.client.post('/api/v1/auth/register/', data, format='json')
        self.assertEqual(request.status_code, 201)

    def test_user_already_existing(self):
        data = {
            "username": "testUser2",
            "email": "testUser2@gmail.com",
            "password1": "testUserPassword123",
            "password2": "testUserPassword123"
        }
        request = self.client.post('/api/v1/auth/register/', data, format='json')
        self.assertEqual(request.status_code, 400)

    def test_email_already_existing(self):
        data = {
            "username": "testUser2",
            "email": "lennon@thebeatles.com",
            "password1": "testUserPassword123",
            "password2": "testUserPassword123"
        }
        request = self.client.post('/api/v1/auth/register/', data, format='json')
        self.assertEqual(request.status_code, 400)

    def test_profile_creation_on_user_creation(self):
        data = {
            "username": "testUser3",
            "email": "testUser3@gmail.com",
            "password1": "testUserPassword123",
            "password2": "testUserPassword123"
        }
        request = self.client.post('/api/v1/auth/register/', data, format='json')
        self.assertEqual(request.status_code, 201)
        self.assertTrue(Profile.objects.get(user=User.objects.get(username='testUser3')))

