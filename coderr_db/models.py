from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class UserProfil(models.Model):
    CATEGORY_CHOICES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    type = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='customer')
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    username = models.CharField(max_length=50, unique=True)
    file = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=25, blank=True)
    tel_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    tel = models.CharField(
        validators=[tel_regex], max_length=17, blank=True
    )
    description = models.CharField(max_length=50, blank=True)
    working_hours = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username