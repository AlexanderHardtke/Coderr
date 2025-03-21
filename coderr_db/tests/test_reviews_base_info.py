from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from coderr_db.models import Review, UserProfil
from .test_data import create_customer_user, create_business_user, create_test_orders, create_test_offers, invalid_review_pk


class ReviewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='customeruser', password='customerpw'
        )
        self.user_profile = create_customer_user(self.user)
        self.business_user = User.objects.create_user(
            username='businessuser', password='businesspassword'
        )
        self.business_user_profile = create_business_user(self.business_user)
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

    def test_duplicate_post_reviews(self):
        data = {
            "business_user": self.business_user_profile,
            "rating": 1,
            "description": "Test post"
        }
        url = reverse('review-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data['created_at'], str)
        response_duplicate = self.client.post(url, data, format='json')
        self.assertEqual(response_duplicate.status_code,
                         status.HTTP_403_FORBIDDEN)

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
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            "business_user": self.business_user_profile,
            "rating": 1,
            "description": "Test post"
        }
        url = reverse('review-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_review_single(self):
        url = reverse('review-detail', kwargs={'pk': 1})
        data = {
            "rating": 5,
            "description": "Noch besser als erwartet!"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['updated_at'], str)

    def test_invalid_patch_review_single(self):
        url = reverse('review-detail', kwargs={'pk': 1})
        data = {
            "error": "Noch besser als erwartet!"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_patch_review_single(self):
        data = {
            "rating": 5,
            "description": "Noch besser als erwartet!"
        }
        self.token = Token.objects.create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        unauthorized_token = 'unauthorized token'
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + unauthorized_token
        )
        url = reverse('review-detail', kwargs={'pk': 1})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_found_patch_review_single(self):
        url = reverse('review-detail', kwargs={'pk': invalid_review_pk})
        data = {
            "rating": 5,
            "description": "Noch besser als erwartet!"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_review_single(self):
        url = reverse('review-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_delete_review_single(self):
        unauthorized_token = 'unauthorized token'
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + unauthorized_token
        )
        url = reverse('review-detail', kwargs={'pk': invalid_review_pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_forbidden_delete_review_single(self):
        self.token = Token.objects.create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('review-detail', kwargs={'pk': invalid_review_pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_found_delete_review_single(self):
        url = reverse('review-detail', kwargs={'pk': invalid_review_pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_base_info(self):
        url = reverse('base-info-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['review_count'], int)
        self.assertIsInstance(response.data['average_rating'], float)
        self.assertIsInstance(response.data['business_profile_count'], float)
        self.assertIsInstance(response.data['offer_count'], int)
