from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
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

        partial_response = {
            "username": "exampleUsername",
            "email": "example@mail.de",
        }
        for key, value in partial_response.items():
            self.assertEqual(response.data[key], value)

        self.assertIsInstance(response.data['token'], str)
        self.assertIsInstance(response.data['user_id'], int)

        response_duplicate = self.client.post(self.url, data, format='json')
        self.assertWarnsMessage(response_duplicate.data,
                                'A user with that username already exists.')

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
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    # Wie schreibe ich einen Test für HTTP_500?
    # def test_false_method(self):
    #     self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('login')

    def test_login_user(self):
        data = {
            "username": "exampleUsername",
            "password": "examplePassword"
        }
        response = self.client.post(self.url, data, format='json')

        for key, value in data.items():
            print(data[key])
            self.assertEqual(data[key], value)

        self.assertIsInstance(response.data['token'], str)
        self.assertIsInstance(response.data['user_id'], int)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_login_user(self):
        data = {
            "username": "wrongUsername",
            "password": "wrongPassword"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)