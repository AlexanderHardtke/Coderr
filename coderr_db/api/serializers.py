from rest_framework import serializers
from coderr_db.models import UserProfil, Offer, Order, Review, OfferDetail
from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound


class RegistrationSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=UserProfil.CATEGORY_CHOICES, write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError(
                {"repeated_password": "Passwörter stimmen nicht überein."}
            )

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {"email": "Diese Email wird bereits verwendet."}
            )

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                {"username": "Dieser Benutzername ist bereits vergeben."}
            )

        return data

    def create(self, validated_data):
        user_type = validated_data.pop('type')
        validated_data.pop('repeated_password')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        UserProfil.objects.create(user=user, type=user_type,)

        return user


class UserProfilSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email')

    class Meta:
        model = UserProfil
        exclude = ['uploaded_at',]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        if 'email' in user_data:
            instance.user.email = user_data['email']
            instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserProfilBusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfil
        exclude = ['created_at', 'uploaded_at']


class UserProfilCustomerSerializer(serializers.ModelSerializer):
    uploaded_at = serializers.ReadOnlyField(source='created_at')
    username = serializers.CharField(source='user.username', read_only=True)

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
            'user': {'required': False}
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
        prices = []
        delivery_times = []
        for detail_data in data:
            price = detail_data.get('price')
            delivery_time = detail_data.get('delivery_time_in_days')
            if price is not None:
                prices.append(price)
            if delivery_time is not None:
                delivery_times.append(delivery_time)
            OfferDetail.objects.create(
                offer=offer, business_user=user, **detail_data)
        offer.min_price = min(prices) if prices else 0
        offer.min_delivery_time = min(delivery_times) if delivery_times else 0
        offer.save()

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

            prices = [d.price for d in instance.details.all()]
            delivery_times = [d.delivery_time_in_days for d in instance.details.all()]

            instance.min_price = min(prices) if prices else 0
            instance.min_delivery_time = min(delivery_times) if delivery_times else 0
            instance.save()

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
                'id': detail.pk,
                'url': request.build_absolute_uri(f'/api/offerdetails/{detail.id}/')
            }
            for detail in obj.details.all()
        ]


class OrderSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='offer_detail.title', read_only=True)
    revisions = serializers.IntegerField(
        source='offer_detail.revisions', read_only=True)
    features = serializers.JSONField(
        source='offer_detail.features', read_only=True)
    offer_type = serializers.CharField(
        source='offer_detail.offer_type', read_only=True)
    offer_detail_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at',
            'offer_detail_id',
        ]
        read_only_fields = [
            'customer_user',
            'delivery_time_in_days',
            'price',
            'created_at',
        ]

    def validate_offer_detail_id(self, data):
        if data is None and not int:
            raise serializers.ValidationError({
                'offer_detail_id': 'Ungültige Anfragedaten, Angebots-ID fehlt.'
            })

        try:
            offer_detail = OfferDetail.objects.get(id=data)
        except OfferDetail.DoesNotExist:
            raise NotFound(
                'Das angegebene Angebotsdetail wurde nicht gefunden.'
            )
        self.context['offer_detail'] = offer_detail
        return data

    def create(self, validated_data):
        offer_detail = self.context['offer_detail']
        validated_data['offer_detail'] = offer_detail
        validated_data['business_user'] = offer_detail.business_user
        validated_data['delivery_time_in_days'] = offer_detail.delivery_time_in_days
        validated_data['price'] = offer_detail.price
        if 'customer_user' not in validated_data:
            validated_data['customer_user'] = self.context['request'].user.userprofil
        return super().create(validated_data)


class OrderCountSerializer(serializers.Serializer):
    order_count = serializers.IntegerField(required=False)
    completed_order_count = serializers.IntegerField(required=False)


class Reviewserializer(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(
        queryset=UserProfil.objects.all())
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'reviewer',
            'created_at',
            'updated_at',
        ]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                'Bewertung muss zwischen 1 und 5 sein.')
        return value

    def validate_business_user(self, value):
        if not UserProfil.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError(
                'Dieser Anbieter existiert nicht.')
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        reviewer = request.user.userprofil
        business_user = validated_data['business_user']
        if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
            raise serializers.ValidationError(
                'Du hast bereits eine Bewertung für diesen Anbieter abgegeben.')
        validated_data['reviewer'] = reviewer
        return super().create(validated_data)
