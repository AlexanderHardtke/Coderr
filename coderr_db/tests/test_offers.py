from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from coderr_db.models import Offer
from coderr_db.api.serializers import OfferSerializer
from .test_data import create_business_user, create_customer_user, create_test_offers, new_offer_data, invalid_offer_pk, patched_offer_data, invalid_offer_data, offer_detail


class OfferTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='businessuser', password='businesspw'
        )
        self.user_profile = create_business_user(self.user)
        self.user_offers = create_test_offers(user=self.user_profile[0])
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('offer-list')

    def test_get_offer_list(self):
        response = self.client.get(self.url, {'min_price': 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        expected_offers = Offer.objects.filter(
            min_price__gte=100).order_by('min_price')
        expected_data = OfferSerializer(expected_offers, many=True).data
        self.assertEqual(results, expected_data)

    def test_wrong_get_offer_list(self):
        response = self.client.get(self.url, {'unvalid_key': 100})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_offer(self):
        response = self.client.post(self.url, new_offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_improper_post_offer(self):
        data = {
            "title": "Zweites Grafikdesign-Paket"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_post_offer(self):
        unauthorized_token = 'unauthorized token'
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + unauthorized_token)
        response = self.client.post(self.url, new_offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_post_offer(self):
        self.user = User.objects.create_user(
            username='customer', password='customerpassword'
        )
        self.user_profile = create_customer_user(self.user)
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(self.url, new_offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_offer_single(self):
        url = reverse('offer-detail', kwargs={'pk': self.user_offers[0].pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_get_offer_single(self):
        unauthorized_token = 'unauthorized token'
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + unauthorized_token)
        url = reverse('offer-detail', kwargs={'pk': self.user_offers[0].pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_found_get_offer_single(self):
        url = reverse('offer-detail', kwargs={'pk': invalid_offer_pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_offer(self):
        url = reverse('offer-detail', kwargs={'pk': self.user_offers[0].pk})
        response = self.client.patch(url, patched_offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "completed")

    def test_invalid_patch_offer(self):
        url = reverse('offer-detail', kwargs={'pk': self.user_offers[0].pk})
        response = self.client.patch(url, invalid_offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_patch_offer(self):
        url = reverse('offer-detail', kwargs={'pk': self.user_offers[0].pk})
        self.user = User.objects.create_user(
            username='customer', password='customerpassword'
        )
        self.user_profile = create_customer_user(self.user)
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.patch(url, patched_offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        unauthorized_token = 'unauthorized token'
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + unauthorized_token)
        response = self.client.patch(url, patched_offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_found_patch_offer(self):
        url = reverse('offer-detail', kwargs={'pk': invalid_offer_pk})
        response = self.client.patch(url, patched_offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_offer(self):
        url = reverse('offer-detail', kwargs={'pk': self.user_offers[0].pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_delete_offer(self):
        url = reverse('offer-detail', kwargs={'pk': self.user_offers[0].pk})
        self.user = User.objects.create_user(
            username='customer', password='customerpassword'
        )
        self.user_profile = create_customer_user(self.user)
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        unauthorized_token = 'unauthorized token'
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + unauthorized_token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_found_delete_offer(self):
        url = reverse('offer-detail', kwargs={'pk': invalid_offer_pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_offer_detail(self):
        url = reverse('offerdetails-detail', kwargs={'pk': offer_detail})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['price'], int)

    def test_unauthorized_get_offer_detail(self):
        unauthorized_token = 'unauthorized token'
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + unauthorized_token)
        url = reverse('offerdetails-detail', kwargs={'pk': offer_detail})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_found_get_offer_detail(self):
        url = reverse('offerdetails-detail', kwargs={'pk': invalid_offer_pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
