from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from coderr_db.models import Review, UserProfil
from coderr_db.api.serializers import ReviewSerializer
from .test_data import new_review_data


class ReviewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.user_profile = UserProfil.objects.create(
            user=self.user,
            username='testuser',
            first_name='Max',
            last_name='Mustermann',
            file='profile_picture.jpg',
            type='customer',
            email='max@customer.de',
            created_at='2023-01-01T12:00:00'
        )
        self.client = APIClient
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('offers-list')

