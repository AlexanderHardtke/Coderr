from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from coderr_db.models import Review, UserProfil
from coderr_db.api.serializers import ReviewSerializer
from .test_data import create_test_orders, create_test_offers


class ReviewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.user_profile = UserProfil.objects.create(
            user=self.user,
            username='testuser',
            first_name='Max',
            last_name='Mustermann',
            file='profile_picture.jpg',
            location='Berlin',
            tel='123456789',
            description='Customer description',
            working_hours='9-17',
            type='customer',
            email='max@customer.de',
            created_at='2023-01-01T12:00:00'
        )
        self.business_user = User.objects.create_user(
            username='businessuser', password='businesspassword'
        )
        self.business_user_profile = UserProfil.objects.create(
            user=self.user,
            username='business',
            first_name='Max',
            last_name='Mustermann',
            file='profile_picture.jpg',
            location='Berlin',
            tel='123456789',
            description='business description',
            working_hours='9-17',
            type='business',
            email='max@business.de',
            created_at='2023-01-01T12:00:00'
        )
        self.user_offers = create_test_offers()
        self.user_orders = create_test_orders()
        self.user_review = Review.objects.create(
            business_user=self.user,
            rating=4,
            description="Alles war toll!"
        )
        self.client = APIClient
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_reviews(self):
        url = reverse('review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "Alles war toll!")

    def test_unauthorized_get_reviews(self):
        unauthorized_token = 'unauthorized token'
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + unauthorized_token)
        url = reverse('review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_reviews(self):
        data = {
            "business_user": self.business_user_profile,
            "rating": 1,
            "description": "Test post"
        }
        url = reverse('review-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data['created_at'], int)

    def test_invalid_post_reviews(self):
        data = {
            "business_user": self.business_user_profile,
            "error": 1,
        }
        url = reverse('review-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_post_reviews(self):
        self.token = Token.objects.create(user=self.business_user)
        data = {
            "business_user": self.business_user_profile,
            "rating": 1,
            "description": "Test post"
        }
        url = reverse('review-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_duplicate_post_reviews(self):
        data = {
            "business_user": self.business_user_profile,
            "rating": 1,
            "description": "Test post"
        }
        url = reverse('review-list')
        response = self.client.post(url, data, format='json')
        response_duplicate = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_review_single(self):
        url = reverse('review-detail')

    def test_delete_review_single(self):
        url = reverse('review-detail')
