from django.urls import reverse
from rest_framework.test import APIClient, APITestCase, force_authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class CreateUserTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('registration-detail')

    def test_create_user(self):
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_duplicate = self.client.post(self.url, data, format='json')
        self.assertWarnsMessage(response_duplicate.data, 'A user with that username already exists.')

    def test_fail_create_user(self):
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "rightPassword",
            "repeated_password": "wrongPassword",
            "type": "customer"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_create_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # WIe schreibe ich einen Test für HTTP_500?
    # def test_false_method(self):
    #     self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class OfferTests(APITestCase):
    pass


class OrderTests(APITestCase):
    pass


class ReviewTests(APITestCase):
    pass
