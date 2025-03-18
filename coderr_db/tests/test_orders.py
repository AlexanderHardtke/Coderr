# from django.urls import reverse
# from rest_framework.test import APITestCase, APIClient
# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
# from coderr_db.models import Order


# class OrdersTests(APITestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(
#             username='testuser', password='testpassword')
#         self.order = Order.objects.create(
#             id=1,
#             customer_user=self.user,
#             business_user=User.objects.create_user(username='businessuser', password='businesspassword'),
#             title="Logo Design",
#             revisions=3,
#             delivery_time_in_days=5,
#             price=150,
#             features=["Logo Design", "Visitenkarten"],
#             offer_type="basic",
#             status="in_progress",
#             created_at=make_aware(datetime(2024, 9, 29, 10, 0, 0)),
#             updated_at=make_aware(datetime(2024, 9, 30, 12, 0, 0))
#         )
#         self.client = APIClient
#         self.token = Token.objects.create(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#         self.url = reverse('orders-list')

#     def test_get_offer(self):
#         url = reverse('offers-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
