from coderr_db.models import Offer, Order

invalid_offer_pk = 66
invalid_order_pk = 66
offer_detail = 4

new_offer_data = {
    "title": "Zweites Grafikdesign-Paket",
    "image": None,
    "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
    "details": [
        {
            "title": "Zweites Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": ["Logo Design", "Visitenkarte"],
            "offer_type": "basic"
        },
        {
            "title": "Zweites Standard Design",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "price": 200,
            "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
            "offer_type": "standard"
        },
        {
            "title": "Zweites Premium Design",
            "revisions": 10,
            "delivery_time_in_days": 10,
            "price": 500,
            "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
            "offer_type": "premium"
        }
    ]
}

patched_offer_data = {
    "title": "patched Grafikdesign-Paket",
    "description": "Ein umfassendes patched Grafikdesign-Paket für Unternehmen.",
    "details": [
        {
            "title": "Zweites patched Basic Design",
            "revisions": 20,
            "delivery_time_in_days": 50,
            "price": 1000,
            "features": ["patched Logo Design", "patched Visitenkarte"],
        }
    ]
}

invalid_offer_data = {
    "id": 1,
    "customer_user": 1,
    "business_user": 2,
    "created_at": "2024-09-29T10:00:00Z",
    "updated_at": "2024-09-30T15:00:00Z"
}

new_review_data = {
    "id": 3,
    "business_user": 2,
    "reviewer": 3,
    "rating": 5,
    "description": "Hervorragende Erfahrung!",
    "created_at": "2023-10-30T15:30:00Z",
    "updated_at": "2023-10-30T15:30:00Z"
}


def create_test_offers():
    return [
        Offer.objects.create(
            title='API-Paket',
            image=None,
            description='Ein umfassendes API-Paket für Unternehmen.',
            details=[
                {
                    "title": "Basic API",
                    "revisions": 2,
                    "delivery_time_in_days": 6,
                    "price": 150,
                    "features": ["Login", "Registrierung"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard API",
                    "revisions": 5,
                    "delivery_time_in_days": 8,
                    "price": 300,
                    "features": ["Login", "Registrierung", "Bearbeitung einfacher Datenstrukturen"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium API",
                    "revisions": 10,
                    "delivery_time_in_days": 15,
                    "price": 750,
                    "features": ["Login", "Registrierung", "Bearbeitung einfacher und komplexer Datenstrukturen"],
                    "offer_type": "premium"
                }
            ]
        ),
        Offer.objects.create(
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
        ),
        Offer.objects.create(
            title='App-Umwandlung',
            image=None,
            description='Ein umwandlung ihrer Website in eine Smartphone-App.',
            details=[
                {
                    "title": "Android",
                    "revisions": 2,
                    "delivery_time_in_days": 3,
                    "price": 100,
                    "features": ["Funktional in Android-Store"],
                    "offer_type": "basic"
                },
                {
                    "title": "Apple-IOS",
                    "revisions": 3,
                    "delivery_time_in_days": 5,
                    "price": 150,
                    "features": ["Funktional in Apple-Store", "Geprüft durch Apple"],
                    "offer_type": "standard"
                },
                {
                    "title": "Android + Apple-IOS",
                    "revisions": 6,
                    "delivery_time_in_days": 7,
                    "price": 225,
                    "features": ["Funktional in Android-Store", "Funktional in Apple-Store", "Geprüft durch Apple"],
                    "offer_type": "premium"
                }
            ]
        )
    ]


def create_test_orders():
    return [
        Order.objects.create(
            customer_user=1,
            business_user=2,
            title="Logo Design",
            revisions=3,
            delivery_time_in_days=5,
            price=150,
            features=[
                "Logo Design",
                "Visitenkarten"
            ],
            offer_type="basic",
            status="in_progress",
            created_at="2024-09-29T10:00:00Z",
            updated_at="2024-09-30T12:00:00Z"
        )
    ]
