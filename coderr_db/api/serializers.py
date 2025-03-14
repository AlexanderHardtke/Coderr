from rest_framework import serializers
from coderr_db.models import UserProfil
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
     
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'repeated_password']
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
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        account.set_password(pw)
        account.save()

        user_profile = UserProfil.objects.create(user=account)

        UserProfil.objects.create(
            user_profile=user_profile,
            email=account.email,
            name=f"{account.first_name} {account.last_name}".strip(),
        )

        return account

class UserProfilSerializer(serializers.ModelSerializer):
    
    class Meta:
         model = UserProfil
         fields = '__all__'