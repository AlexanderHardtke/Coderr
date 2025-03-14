from django.db import models
from django.contrib.auth.models import User


class UserProfil(models.Model):
    CATEGORY_CHOICES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='customer')
    email = models.EmailField(max_length=50)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    username = first_name + ' ' + last_name