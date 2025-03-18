from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from coderr_db.models import Offer


class OfferTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.user_Offer = Offer.objects.create(
            title='Grafikdesign-Paket',
            image=None,
            description='Ein umfassendes Grafikdesign-Paket für Unternehmen.',
            details=[
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
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

        # Überprüfen der Antwortstruktur
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

        # Überprüfen der Inhalte
        results = response.data['results']
        self.assertEqual(len(results), 1)

        offer = results[0]
        self.assertEqual(offer['id'], self.user_offer.id)
        self.assertEqual(offer['title'], self.user_offer.title)
        self.assertEqual(offer['description'], self.user_offer.description)
        self.assertEqual(offer['image'], self.user_offer.image)
        self.assertEqual(offer['min_price'], 100)  # Beispielwert, anpassen
        self.assertEqual(offer['min_delivery_time'], 5)  # Beispielwert, anpassen

        # Überprüfen der user_details
        self.assertIn('user_details', offer)
        user_details = offer['user_details']
        self.assertEqual(user_details['first_name'], self.user.first_name)
        self.assertEqual(user_details['last_name'], self.user.last_name)
        self.assertEqual(user_details['username'], self.user.username)

        # Überprüfen der details
        self.assertIn('details', offer)
        details = offer['details']
        self.assertEqual(len(details), 3)

        # Beispiel: Überprüfen des ersten Details
        first_detail = details[0]
        self.assertEqual(first_detail['id'], 1)
        self.assertEqual(first_detail['url'], '/offerdetails/1/')

    def test_post_offer(self):
        data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
                    "offer_type": "premium"
                }
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)