from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from coderr_db.models import Order, UserProfil
from .test_data import create_test_orders, create_test_offers, create_customer_user, create_business_user, invalid_order_pk


class OrderTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='customeruser', password='customerpw'
        )
        self.user_profile = create_customer_user(self.user)
        self.business_user = User.objects.create_user(
            username='businessuser', password='businesspw'
        )
        self.business_profile = create_business_user(self.business_user)
        self.user_offers = create_test_offers(user=self.business_profile[0])
        self.user_orders = create_test_orders(user=self.user_profile[0])
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('orders-list')

    # def test_get_order_list(self):
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     first_order = response.data[0]
    #     self.assertEqual(first_order['customer_user'], self.user.pk)

    # def test_unauthorized_get_order_list(self):
    #     unauthorized_token = 'unauthorized token'
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Token ' + unauthorized_token
    #     )
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_post_order(self):
    #     data = {"offer_detail_id": 1}
    #     response = self.client.post(self.url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_invalid_post_order(self):
    #     data = {"offer_error_id": 1}
    #     response = self.client.post(self.url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_unauthorized_post_order(self):
    #     data = {"offer_detail_id": 1}
    #     self.token = Token.objects.create(user=self.business_user)
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    #     response = self.client.post(self.url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #     unauthorized_token = 'unauthorized token'
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Token ' + unauthorized_token
    #     )
    #     response = self.client.post(self.url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_invalid_post_order(self):
    #     data = {"offer_detail_id": invalid_order_pk}
    #     response = self.client.post(self.url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_patch_order(self):
    #     self.token = Token.objects.create(user=self.business_user)
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    #     url = reverse('orders-detail', kwargs={'pk': self.user_orders[0].pk})
    #     data = {"status": "completed"}
    #     response = self.client.patch(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data["status"], "completed")

    # def test_invalid_patch_order(self):
    #     self.token = Token.objects.create(user=self.business_user)
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    #     url = reverse('orders-detail', kwargs={'pk': self.user_orders[0].pk})
    #     invalid_data = {"status": "error"}
    #     response = self.client.patch(url, invalid_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_unauthorized_patch_order(self):
    #     data = {"status": "completed"}
    #     url = reverse('orders-detail', kwargs={'pk': self.user_orders[0].pk})
    #     response = self.client.patch(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #     unauthorized_token = 'unauthorized token'
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Token ' + unauthorized_token
    #     )
    #     response = self.client.patch(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_not_found_patch_order(self):
    #     data = {"status": "completed"}
    #     url = reverse('orders-detail', kwargs={'pk': invalid_order_pk})
    #     response = self.client.patch(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order(self):
        self.admin = User.objects.create_superuser(username='staff', password='staffpw', is_staff=True)
        self.client.force_authenticate(user=self.admin)
        url = reverse('orders-detail', kwargs={'pk': self.user_orders[0].pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_delete_order(self):
        url = reverse('orders-detail', kwargs={'pk': self.user_orders.pk})
        self.user = User.objects.create_user(
            username='otherUser', password='otherUser'
        )
        self.user_profile = create_customer_user(self.user)
        self.client = APIClient
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        unauthorized_token = 'unauthorized token'
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + unauthorized_token
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_found_delete_order(self):
        url = reverse('orders-detail', kwargs={'pk': invalid_order_pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_order_count_detail(self):
    #     url = reverse('order-count-detail', kwargs={'pk': self.user.pk})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIsInstance(response.data['order_count'], int)

    # def test_unauthorized_order_count_detail(self):
    #     unauthorized_token = 'unauthorized token'
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Token ' + unauthorized_token
    #     )
    #     url = reverse('order-count-detail', kwargs={'pk': self.user.pk})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_not_found_order_count_detail(self):
    #     url = reverse('order-count-detail', kwargs={'pk': invalid_order_pk})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_order_count_completed_detail(self):
    #     url = reverse(
    #         'completed-order-count-detail', kwargs={'pk': self.user.pk}
    #     )
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIsInstance(response.data['completed_order_count'], int)

    # def test_unauthorized_order_count_completed_detail(self):
    #     url = reverse(
    #         'completed-order-count-detail', kwargs={'pk': invalid_order_pk}
    #     )
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_not_found_order_count_completed_detail(self):
    #     url = reverse(
    #         'completed-order-count-detail', kwargs={'pk': invalid_order_pk}
    #     )
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)