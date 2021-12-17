import tempfile

from django.test import TestCase
import PIL
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from reviews.models import Review

# Create your tests here.


class ReviewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.buyer = User.objects.create_user('testUser2', 'lennon@thebeatles.com', 'johnpassword')
        self.seller = User.objects.create_user('testUser3', 'lennon2@thebeatles.com', 'johnpassword')
        self.token = Token.objects.get_or_create(user=self.buyer)[0].__str__()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_patch_review(self):
        r = Review.objects.create(reviewer=self.buyer, seller=self.seller, message="test", val=3)
        r.save()
        data = {
            'message': 'test2',
            'val': 4,
            'check': False
        }
        url = "/api/v1/reviews/?seller=" + self.seller.username
        request = self.client.patch(url, data)
        rev = Review.objects.get(reviewer=self.buyer, seller=self.seller)

        assert request.data['message'] == rev.message
        assert request.data['val'] == rev.val
        assert request.status_code == 200

    def test_patch_review_wrong_user(self):
        r = Review.objects.create(reviewer=self.buyer, seller=self.seller, message="test", val=3)
        r.save()
        data = {
            'message': 'test2',
            'val': 4,
            'check': False
        }
        url = "/api/v1/reviews/?seller=haha"
        request = self.client.patch(url, data)

        assert request.data == 'Buyer or Seller not found'
        assert request.status_code == 404

    def test_patch_review_wrong_review(self):
        data = {
            'message': 'test2',
            'val': 4,
            'check': False
        }
        url = "/api/v1/reviews/?seller=" + self.seller.username
        request = self.client.patch(url, data)

        assert request.data == 'Review not found'
        assert request.status_code == 404

    def test_patch_review_bad_rquest(self):
        r = Review.objects.create(reviewer=self.buyer, seller=self.seller, message="test", val=3)
        r.save()
        data = {
            'val': 'casi crack'
        }
        url = "/api/v1/reviews/?seller=" + self.seller.username
        request = self.client.patch(url, data)
        assert request.data == 'Bad Request :('
        assert request.status_code == 400

    def test_post_review(self):
        url = "/api/v1/reviews/?seller=" + self.seller.username
        data = {
            "message": "test",
            "val": 5
        }
        request = self.client.post(url, data)
        review = Review.objects.get(seller=self.seller, message="test")

        assert review
        assert review.message == "test"
        assert review.val == 5
        assert request.status_code == 200

    def test_post_review_no_seller(self):
        url = "/api/v1/reviews/"
        data = {
            "message": "test",
            "val": 5
        }
        request = self.client.post(url, data)

        assert request.data == 'Seller not provided'
        assert request.status_code == 400

    def test_post_review_wrong_seller(self):
        url = "/api/v1/reviews/?seller=hahaha"
        data = {
            "message": "test",
            "val": 5
        }
        request = self.client.post(url, data)

        assert request.data == "Couldn't find seller"
        assert request.status_code == 404

    def test_post_review_error_creating_review(self):
        url = "/api/v1/reviews/?seller=" + self.seller.username
        data = {
            "message": "test",
            "val": "casi crack"
        }
        request = self.client.post(url, data)

        assert request.data == "Couldn't create review"
        assert request.status_code == 500

    def test_get_reviews(self):
        url = "/api/v1/reviews/?seller=" + self.seller.username
        r = Review.objects.create(reviewer=self.buyer, seller=self.seller, message="test", val=3)
        r.check = True
        r.save()

        request = self.client.get(url)

        assert request.data[0]['message'] == "test"
        assert request.data[0]['val'] == 3
        assert request.status_code == 200

    def test_get_reviews_no_content(self):
        url = "/api/v1/reviews/?seller=" + self.seller.username
        r = Review.objects.create(reviewer=self.buyer, seller=self.seller, message="test", val=3)
        r.save()

        request = self.client.get(url)

        assert not request.data
        assert request.status_code == 204

    def test_get_reviews_no_seller(self):
        url = "/api/v1/reviews/"
        r = Review.objects.create(reviewer=self.buyer, seller=self.seller, message="test", val=3)
        r.save()

        request = self.client.get(url)
        assert request.data == 'Seller not provided'
        assert request.status_code == 400

    def test_my_reviews_no_content(self):
        url = "/api/v1/reviews/myreviews/"

        request = self.client.get(url)
        assert request.data == []
        assert request.status_code == 204

    def test_my_reviews(self):
        url = "/api/v1/reviews/myreviews/"

        r = Review.objects.create(reviewer=self.buyer, seller=self.seller, message='test', val=3)
        r.check = True
        r.save()

        request = self.client.get(url)
        assert request.data[0]['message'] == 'test'
        assert request.status_code == 200