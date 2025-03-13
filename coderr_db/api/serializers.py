from rest_framework import serializers
from coderr_db.models import UserProfil
from django.contrib.auth.models import User


class UserProfilSerializer(serializers.ModelSerializer):
    
    class Meta:
         model = UserProfil
         fields = '__all__'