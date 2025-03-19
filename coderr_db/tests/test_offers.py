from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from coderr_db.models import Offer, UserProfil
from coderr_db.api.serializers import OfferSerializer
from .test_data import create_test_offers, new_offer_data


class OfferTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.user_profile = UserProfil.objects.create(
                user= self.user,
                username= 'testuser',
                first_name= 'Max',
                last_name= 'Mustermann',
                file= 'profile_picture.jpg',
                location= 'Berlin',
                tel= '123456789',
                description= 'Business description',
                working_hours= '9-17',
                type= 'business',
                email= 'max@business.de',
                created_at= '2023-01-01T12:00:00'
        )
        self.user_offers = create_test_offers()
        self.client = APIClient
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('offers-list')

    def test_get_offer(self):
        response = self.client.get(self.url, {'min_price': 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        expected_offers = Offer.objects.filter(min_price__gte=100).order_by('min_price')
        expected_data = OfferSerializer(expected_offers, many=True).data
        self.assertEqual(results, expected_data)

    def test_wrong_get_offer(self):
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
        self.client = APIClient
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(self.url, new_offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    