from coderr_db.models import Offer, Order, UserProfil, OfferDetail
from django.contrib.auth.models import User


invalid_offer_pk = 254
invalid_order_pk = 254
invalid_review_pk = 254
offer_detail = 4

new_offer_data = {
    'title': 'Zweites Grafikdesign-Paket',
    'image': None,
    'description': 'Ein umfassendes Grafikdesign-Paket für Unternehmen.',
    'details': [
        {
            'title': 'Zweites Basic Design',
            'revisions': 2,
            'delivery_time_in_days': 5,
            'price': 100,
            'features': ['Logo Design', 'Visitenkarte'],
            'offer_type': 'basic'
        },
        {
            'title': 'Zweites Standard Design',
            'revisions': 5,
            'delivery_time_in_days': 7,
            'price': 200,
            'features': ['Logo Design', 'Visitenkarte', 'Briefpapier'],
            'offer_type': 'standard'
        },
        {
            'title': 'Zweites Premium Design',
            'revisions': 10,
            'delivery_time_in_days': 10,
            'price': 500,
            'features': ['Logo Design', 'Visitenkarte', 'Briefpapier', 'Flyer'],
            'offer_type': 'premium'
        }
    ]
}

patched_offer_data = {
  'title': 'Updated Grafikdesign-Paket',
  'details': [
    {
      'title': 'Basic Design Updated',
      'revisions': 3,
      'delivery_time_in_days': 6,
      'price': 120,
      'features': [
        'Logo Design',
        'Flyer'
      ],
      'offer_type': 'basic'
    }
  ]
}

invalid_offer_data = {
  'title': 'Updated Grafikdesign-Paket',
  'details': [
    {
      'title': 'Basic Design Updated',
      'offer_type': 'error'
    }
  ]
}

new_review_data = {
    'id': 3,
    'business_user': 2,
    'reviewer': 3,
    'rating': 5,
    'description': 'Hervorragende Erfahrung!',
    'created_at': '2023-10-30T15:30:00Z',
    'updated_at': '2023-10-30T15:30:00Z'
}


def create_test_offers(user):
    offer1 = Offer.objects.create(
        title='API-Paket',
        image=None,
        description='Ein umfassendes API-Paket für Unternehmen.',
        user=user
    )
    
    offer2 = Offer.objects.create(
        title='Grafikdesign-Paket',
        image=None,
        description='Ein umfassendes Grafikdesign-Paket für Unternehmen.',
        user=user
    )
    
    offer3 = Offer.objects.create(
        title='App-Umwandlung',
        image=None,
        description='Ein umwandlung ihrer Website in eine Smartphone-App.',
        user=user
    )
    
    OfferDetail.objects.create(
        business_user_id=user.id,
        offer=offer1,
        title='Basic API',
        revisions=2,
        delivery_time_in_days=6,
        price=150,
        features=['Login', 'Registrierung'],
        offer_type='basic'
    )
    OfferDetail.objects.create(
        business_user_id=user.id,
        offer=offer1,
        title='Standard API',
        revisions=5,
        delivery_time_in_days=8,
        price=300,
        features=['Login', 'Registrierung', 'Bearbeitung einfacher Datenstrukturen'],
        offer_type='standard'
    )
    OfferDetail.objects.create(
        business_user_id=user.id,
        offer=offer1,
        title='Premium API',
        revisions=10,
        delivery_time_in_days=15,
        price=750,
        features=['Login', 'Registrierung', 'Bearbeitung einfacher und komplexer Datenstrukturen'],
        offer_type='premium'
    )
    
    OfferDetail.objects.create(
        business_user_id=user.id,
        offer=offer2,
        title='Basic Design',
        revisions=2,
        delivery_time_in_days=5,
        price=100,
        features=['Logo Design', 'Visitenkarte'],
        offer_type='basic'
    )
    OfferDetail.objects.create(
        business_user_id=user.id,
        offer=offer2,
        title='Standard Design',
        revisions=5,
        delivery_time_in_days=7,
        price=200,
        features=['Logo Design', 'Visitenkarte', 'Briefpapier'],
        offer_type='standard'
    )
    OfferDetail.objects.create(
        business_user_id=user.id,
        offer=offer2,
        title='Premium Design',
        revisions=10,
        delivery_time_in_days=10,
        price=500,
        features=['Logo Design', 'Visitenkarte', 'Briefpapier', 'Flyer'],
        offer_type='premium'
    )
    
    OfferDetail.objects.create(
        business_user_id=user.id,
        offer=offer3,
        title='Android',
        revisions=2,
        delivery_time_in_days=3,
        price=100,
        features=['Funktional in Android-Store'],
        offer_type='basic'
    )
    OfferDetail.objects.create(
        business_user_id=user.id,
        offer=offer3,
        title='Apple-IOS',
        revisions=3,
        delivery_time_in_days=5,
        price=150,
        features=['Funktional in Apple-Store', 'Geprüft durch Apple'],
        offer_type='standard'
    )
    OfferDetail.objects.create(
        business_user_id=user.id,
        offer=offer3,
        title='Android + Apple-IOS',
        revisions=6,
        delivery_time_in_days=7,
        price=225,
        features=['Funktional in Android-Store', 'Funktional in Apple-Store', 'Geprüft durch Apple'],
        offer_type='premium'
    )
    
    return [offer1, offer2, offer3]


def create_test_orders(user):
    offer_detail = OfferDetail.objects.first()

    return [
        Order.objects.create(
            customer_user=user,
            business_user=offer_detail.business_user,
            offer_detail=offer_detail,
            status='in_progress',
            price=offer_detail.price,
            delivery_time_in_days=offer_detail.delivery_time_in_days
        )
    ]

def create_business_user(user):
    return [
        UserProfil.objects.create(
                user= user,
                first_name= 'Max',
                last_name= 'Mustermann',
                file= 'profile_picture.jpg',
                location= 'Berlin',
                tel= '123456789',
                description= 'Business description',
                working_hours= '9-17',
                type= 'business',
                created_at= '2023-01-01T12:00:00'
        )
    ]

def create_duplicate_business_user(user):
    return [
        UserProfil.objects.create(
                user= user,
                first_name= 'duplicate',
                last_name= 'duplicate',
                file= 'duplicate.jpg',
                location= 'duplicate',
                tel= '123456789',
                description= 'duplicate description',
                working_hours= '9-17',
                type= 'business',
                created_at= '2023-01-01T12:00:00'
        )
    ]

def create_customer_user(user):
    return [
        UserProfil.objects.create(
                user= user,
                first_name= 'Jane',
                last_name= 'Doe',
                file= 'profile_picture.jpg',
                location= 'Berlin',
                tel= '123456789',
                description= 'customer description',
                working_hours= '9-17',
                type= 'customer',
                created_at= '2023-01-01T12:00:00'
        )
    ]