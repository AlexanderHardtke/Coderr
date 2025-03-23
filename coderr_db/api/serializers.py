from rest_framework import serializers
from coderr_db.models import UserProfil, Offer, Order, Review, BaseInfo
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
     
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'passwords dont match'})
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'email already used'})
        
        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        account.set_password(pw)
        account.save()

        UserProfil.objects.create(
            user=account,
            email=account.email,
            username=account.username
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
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'uploaded_at', 'type']


class OfferSerializer(serializers.ModelSerializer):

    details = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Offer
        fields = '__all__'


class OfferHyperlinkedSerializer(OfferSerializer, serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Offer
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = '__all__'


class Reviewserializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = '__all__'


class BaseInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BaseInfo
        fields = '__all__'