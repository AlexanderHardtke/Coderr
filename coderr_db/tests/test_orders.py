from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from coderr_db.models import Order, UserProfil
from coderr_db.api.serializers import OrderSerializer
from .test_data import create_test_orders, create_test_offers, invalid_order_pk


class OrderTests(APITestCase):

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
        self.user_offers = create_test_offers()
        self.user_orders = create_test_orders()
        self.client = APIClient
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('orders-list')

    def test_get_order_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response.data, self.user)

    def test_unauthorized_get_order_list(self):
        unauthorized_token = 'unauthorized token'
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + unauthorized_token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_order(self):
        data = {
            "offer_detail_id": 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_order(self):
        data = {
            "offer_error_id": 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_post_order(self):
        data = {
            "offer_detail_id": 1
        }
        self.user = User.objects.create_user(
            username='business', password='business'
        )
        self.user_profile = UserProfil.objects.create(
            user=self.user,
            username='testuser',
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
        self.client = APIClient
        self.token = Token.objects.create(user=self.user)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        unauthorized_token = 'unauthorized token'
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + unauthorized_token)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_post_order(self):
        response = self.client.post(self.url, invalid_order_pk, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_order(self):
        url = reverse('orders-detail', kwargs={'pk': self.user_orders.pk})
        data = {
            "status": "completed"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "completed")

    def test_invalid_patch_order(self):
        url = reverse('orders-detail', kwargs={'pk': self.user_orders.pk})
        invalid_data = {
            "status": "error"
        }
        response = self.client.patch(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_patch_order(self):
        data = {
            "status": "completed"
        }
        url = reverse('orders-detail', kwargs={'pk': self.user_orders.pk})
        self.user = User.objects.create_user(
            username='business', password='business'
        )
        self.user_profile = UserProfil.objects.create(
            user=self.user,
            username='testuser',
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
        self.client = APIClient
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        unauthorized_token = 'unauthorized token'
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + unauthorized_token)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_found_patch_order(self):
        data = {
            "status": "completed"
        }
        url = reverse('orders-detail', kwargs={'pk': invalid_order_pk})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order(self):
        url = reverse('orders-detail', kwargs={'pk': self.user_orders.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_delete_order(self):
        url = reverse('orders-detail', kwargs={'pk': self.user_orders.pk})
        self.user = User.objects.create_user(
            username='otherUser', password='otherUser'
        )
        self.user_profile = UserProfil.objects.create(
            user=self.user,
            username='otherUser',
            first_name='Max',
            last_name='Mustermann',
            file='profile_picture.jpg',
            location='Berlin',
            tel='123456789',
            description='otherUser description',
            working_hours='9-17',
            type='customer',
            email='max@other.de',
            created_at='2023-01-01T12:00:00'
        )
        self.client = APIClient
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        unauthorized_token = 'unauthorized token'
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + unauthorized_token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_found_delete_order(self):
        url = reverse('orders-detail', kwargs={'pk': invalid_order_pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    