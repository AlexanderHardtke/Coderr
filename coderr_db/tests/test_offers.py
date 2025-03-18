from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from coderr_db.models import Offer


class OfferTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client = APIClient
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('')

    def test_get_offer(self):
        url = reverse('offers-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
