from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class ProfilSingleTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('profile-detail')


class ProfilBusinessTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('profile_business-list')


class ProfilCustomerTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('profile_customer-list')