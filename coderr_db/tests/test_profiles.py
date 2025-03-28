from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .test_data import create_business_user, create_customer_user
from datetime import datetime


class ProfileTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='businessuser', password='businesspw'
        )
        self.user_profile = create_business_user(self.user)
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_single_profile(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_unauthorized_user(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.pk})
        unauthorized_token = 'unauthorized token'
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + unauthorized_token)
        self.user = User.objects
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_not_found(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.pk+1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_profile(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.pk})
        data = {
            "first_name": "firstTest",
            "last_name": "lastTest"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.data['first_name'], "firstTest")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for key, value in data.items():
            self.assertEqual(response.data[key], value)

        self.assertIsInstance(response.data['user'], int)
        self.assertIsInstance(response.data['username'], str)
        self.assertIsInstance(response.data['file'], str)
        self.assertIsInstance(response.data['type'], str)
        self.assertIsInstance(response.data['created_at'], str)

    def test_update_unauthorized_user(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.pk})
        unauthorized_token = 'unauthorized token'
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + unauthorized_token
        )
        self.user = User.objects
        data = {"first_name": "error"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile_not_found(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.pk+1})
        data = {"first_name": "error"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_owner(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.pk})
        self.user = User.objects.create_user(
            username='otherUser',
            password='otherPassword',
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {"first_name": "error"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_business_profiles(self):
        url = reverse('profiles-business-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Mustermann')
        self.assertIsInstance(response.data[0]['working_hours'], str)

    def test_get_customer_profiles(self):
        self.test_user = User.objects.create_user(
            username='customeruser', password='customerpw'
        )
        self.user_profile = create_customer_user(self.test_user)
        url = reverse('profiles-customer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'customer')
        self.assertIsInstance(response.data[0]['uploaded_at'], datetime)

    def test_unauthorized_profiles(self):
        unauthorized_token = 'unauthorized token'
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + unauthorized_token
        )
        url = reverse('profiles-business-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        url = reverse('profiles-customer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
