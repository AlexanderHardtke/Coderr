from rest_framework import serializers
from coderr_db.models import UserProfil, Offer, Order, Review, BaseInfo, OfferDetail
from django.contrib.auth.models import User
from .permissions import IsCustomerUser


class RegistrationSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=UserProfil.CATEGORY_CHOICES, write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        user_type = self.validated_data.pop('type')

        if pw != repeated_pw:
            raise serializers.ValidationError(
                {'error': 'Passwörter stimmen nicht überein.'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email wird bereits verwendet.'})

        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        
        account.set_password(pw)
        account.save()

        UserProfil.objects.create(
            user=account,
            email=account.email,
            username=account.username,
            type=user_type, 
        )

        return account


class UserProfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfil
        fields = '__all__'


class UserProfilBusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfil
        exclude = ['email', 'created_at', 'uploaded_at']


class UserProfilCustomerSerializer(serializers.ModelSerializer):
    uploaded_at = serializers.ReadOnlyField(source='created_at')

    class Meta:
        model = UserProfil
        fields = ['user', 'username', 'first_name',
                  'last_name', 'file', 'uploaded_at', 'type']


class OfferDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferDetail
        exclude = ['url', 'offer', 'business_user']


class OfferSerializer(serializers.ModelSerializer):

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = '__all__'
        extra_kwargs = {
            "user": {"required": False}
        }

    def validate(self, data):
        data = super().validate(data)
        if 'details' in data:
            valid_offer_types = {'basic', 'standard', 'premium'}
            details_data = data['details']
            for detail_data in details_data:
                offer_type = detail_data.get('offer_type')
                if offer_type is None:
                    raise serializers.ValidationError({
                        'details': 'Ungültige Anfragedaten oder unvollständige Details.'
                    })
                if offer_type not in valid_offer_types:
                    raise serializers.ValidationError({
                        'details': 'Ungültige Anfragedaten oder unvollständige Details.'
                    })

        return data

    def create(self, validated_data):
        data = validated_data.pop('details')
        user = validated_data['user']
        offer = Offer.objects.create(**validated_data)
        for detail_data in data:
            OfferDetail.objects.create(offer=offer, business_user=user, **detail_data)
        return offer

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()

        if 'details' in validated_data:
            details = instance.details.all()
            existing_details = {
                detail.offer_type: detail for detail in details}
            data = validated_data['details']

            for detail_data in data:
                offer_type = detail_data.get('offer_type')
                if offer_type in existing_details:
                    detail_instance = existing_details[offer_type]
                    for attr, value in detail_data.items():
                        setattr(detail_instance, attr, value)
                    detail_instance.save()
                else:
                    OfferDetail.objects.create(offer=instance, **detail_data)

        return instance


class OfferGetSerializer(serializers.ModelSerializer):

    details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = '__all__'

    def get_details(self, obj):
        request = self.context.get('request')
        return [
            {
                "id": detail.pk,
                "url": request.build_absolute_uri(f"/api/offerdetails/{detail.id}/")
            }
            for detail in obj.details.all()
        ]


class OrderSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="offer_detail.title", read_only=True)
    revisions = serializers.IntegerField(source="offer_detail.revisions", read_only=True)
    features = serializers.JSONField(source="offer_detail.features", read_only=True)
    offer_type = serializers.CharField(source="offer_detail.offer_type", read_only=True)
    offer_detail_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
            "offer_detail_id",
        ]
        read_only_fields = [
            "customer_user",
            "delivery_time_in_days",
            "price",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        offer_detail_id = data.get('offer_detail_id')
        if offer_detail_id is None:
            raise serializers.ValidationError({
                'offer_detail_id': 'Ungültige Anfragedaten, Angebots-ID fehlt.'
            })

        try:
            offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError({
                'offer_detail_id': 'Ungültige Angebots-ID. Das Angebot existiert nicht.'
            })
        
        data['offer_detail'] = offer_detail
        print("Business User in validate:", offer_detail.business_user)
        data['business_user'] = offer_detail.business_user
        data['delivery_time_in_days'] = offer_detail.delivery_time_in_days
        data['price'] = offer_detail.price
        return data
    
    def create(self, validated_data):
        print("Business User before create:", validated_data.get('business_user'))
        if 'customer_user' not in validated_data:
            validated_data['customer_user'] = self.context['request'].user.userprofil
            validated_data['business_user'] = validated_data['offer_detail'].business_user
        return super().create(validated_data)


class Reviewserializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class BaseInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseInfo
        fields = '__all__'
