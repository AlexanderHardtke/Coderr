# from django.urls import reverse
# from rest_framework.test import APIClient, APITestCase
# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User


# class ProfileTests(APITestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(
#             username='businessUser',
#             password='businesspassword',
#         )
#         self.user = User.objects.create_user(
#             username='customerUser', password='customerpassword')
        
#     def test_get_single_profile(self):
#         url = reverse('profile-detail', kwargs={'pk': self.user.pk})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_update_profile(self):
#         url = reverse('profile-detail', kwargs={'pk': self.user.pk})
#         data = {
#             "first_name": "firstTest",
#             "last_name": "lastTest",
#             "location": "Testhausen",
#             "tel": "987654321",
#             "description": "Test description",
#             "working_hours": "10-18",
#             "email": "new_email@business.de"
#         }
#         response = self.client.patch(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         for key, value in data.items():
#             self.assertEqual(response.data[key], value)

#         self.assertIsInstance(response.data['user'], int)
#         self.assertIsInstance(response.data['username'], str)
#         self.assertIsInstance(response.data['file'], str)
#         self.assertIsInstance(response.data['type'], str)
#         self.assertIsInstance(response.data['created_at'], str)

#     def test_unauthorized_user(self):
#         url = reverse('profile-detail', kwargs={'pk': self.user.pk})
#         self.user = User.objects
#         response = self.client.get(url)

#     def test_unauthorized_owner(self):
#         url = reverse('profile-detail', kwargs={'pk': self.user.pk})
#         self.user = User.objects.create_user(
#             username='otherUser',
#             password='otherPassword',
#         )
#         response = self.client.patch(url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_user_not_found(self):
#         pass
