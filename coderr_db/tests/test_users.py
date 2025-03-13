from django.urls import reverse
from rest_framework.test import APIClient, APITestCase, force_authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class BusinessProfile(APITestCase):
    pass