from rest_framework import serializers
from coderr_db.models import BusinessUserProfile, CustomerUserProfile
from django.contrib.auth.models import User


class BusinessUserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
         model = BusinessUserProfile
         fields = '__all__'

class CustomerUserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
         model = CustomerUserProfile
         fields = '__all__'
