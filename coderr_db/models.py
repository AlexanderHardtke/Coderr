from django.db import models
from django.contrib.auth.models import User


class UserProfil(models.Model):
    CATEGORY_CHOICES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='customer')