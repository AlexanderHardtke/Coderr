from django.urls import reverse
from rest_framework.test import APIClient, APITestCase, force_authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class UserTests(APITestCase):

    def test_create_user(self):
        self.client = APIClient()
        url = reverse('registration-detail')
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class OfferTests(APITestCase):
    pass


class OrderTests(APITestCase):
    pass


class ReviewTests(APITestCase):
    pass
