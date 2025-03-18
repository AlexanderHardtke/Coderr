from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from coderr_db.models import UserProfil


class ProfileTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
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
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + unauthorized_token)
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
            "last_name": "lastTest",
            "location": "Testhausen",
            "tel": "987654321",
            "description": "Test description",
            "working_hours": "10-18",
            "email": "new_email@business.de"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for key, value in data.items():
            self.assertEqual(response.data[key], value)

        # Sieht irgendwie schlecht aus
        self.assertIsInstance(response.data['user'], int)
        self.assertIsInstance(response.data['username'], str)
        self.assertIsInstance(response.data['file'], str)
        self.assertIsInstance(response.data['type'], str)
        self.assertIsInstance(response.data['created_at'], str)

    # Wie schreibe ich einen Test für HTTP_500?
    # def test_false_method(self):
    #     self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    #sind irgendwie doppelt einmal für get und einmal für patch
    def test_update_unauthorized_user(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.pk})
        unauthorized_token = 'unauthorized token'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + unauthorized_token)
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
        self.assertIsInstance(response.data['working_hours'], str)

    def test_get_customer_profiles(self):
        self.test_user = User.objects.create_user(username='customer', password='testpassword')
        self.user_profile = UserProfil.objects.create(
                user= self.test_user,
                username= 'customer',
                first_name= 'test',
                last_name= 'customeruser',
                file= 'profile_picture_customer.jpg',
                uploaded_at= '2023-09-15T09:00:00',
                type= 'customer'
        )

        url = reverse('profiles-customer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'customeruser')
        self.assertIsInstance(response.data['uploaded_at'], str)

    def test_unauthorized_profiles(self):
        unauthorized_token = 'unauthorized token'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + unauthorized_token)
        url = reverse('profiles-business-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        url = reverse('profiles-customer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
