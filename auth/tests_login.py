from django.test import TestCase
from rest_framework.authtoken.admin import User
from rest_framework.test import APIClient


class LoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.u = User.objects.create_user('testUser2', 'lennon@thebeatles.com', 'johnpassword')


    def test_login_success(self):
        data={
            'username': 'testUser2',
            'password': 'johnpassword'
        }
        response = self.client.post('/api/v1/auth/login/', data, format='json')
        self.assertEqual(response.status_code, 200)  # 200 es OK

    def test_login_failed_no_username(self):
        data = {
            'username': '',
            'password': 'johnpassword'
        }
        response = self.client.post('api/v1/auth/login/', data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_login_failed_no_password(self):
        data = {
            'username': 'testUser2',
            'password': ''
        }
        response = self.client.post('/api/v1/auth/login/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_login_failed_wrong_password(self):
        data = {
            'username': 'testUser2',
            'password': '123'
        }
        response = self.client.post('/api/v1/auth/login/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_login_failed_wrong_username(self):
        data = {
            'username': '1234',
            'password': 'johnpassword'
        }
        response = self.client.post('/api/v1/auth/login/', data, format='json')
        self.assertEqual(response.status_code, 400)