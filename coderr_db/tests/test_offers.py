from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from coderr_db.models import Offer


class OfferTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_Offer = Offer.objects.create(
                title = 'Grafikdesign-Paket',
                image = None,
                description = 'Ein umfassendes Grafikdesign-Paket für Unternehmen.',
                details = [
                    {
                        "title": "Basic Design",
                        "revisions": 2,
                        "delivery_time_in_days": 5,
                        "price": 100,
                        "features": [
                            "Logo Design",
                            "Visitenkarte"
                        ],
                        "offer_type": "basic"
                    },
                    {
                        "title": "Standard Design",
                        "revisions": 5,
                        "delivery_time_in_days": 7,
                        "price": 200,
                        "features": [
                            "Logo Design",
                            "Visitenkarte",
                            "Briefpapier"
                        ],
                        "offer_type": "standard"
                    },
                    {
                        "title": "Premium Design",
                        "revisions": 10,
                        "delivery_time_in_days": 10,
                        "price": 500,
                        "features": [
                            "Logo Design",
                            "Visitenkarte",
                            "Briefpapier",
                            "Flyer"
                        ],
                        "offer_type": "premium"
                    }
                ]
        )
        self.client = APIClient
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('offers-list')

    def test_get_offer(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
