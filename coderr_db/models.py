from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfil(models.Model):
    CATEGORY_CHOICES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    type = models.CharField(
        max_length=10, choices=CATEGORY_CHOICES, null=False, blank=False)
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
    description = models.CharField(max_length=255, blank=True)
    working_hours = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    # uploaded_at = #ist das nicht updated at?


class Offer(models.Model):
    user = models.ForeignKey(
        UserProfil, on_delete=models.CASCADE, related_name="offers"
    )
    title = models.CharField(max_length=50)
    image = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OfferDetail(models.Model):
    business_user = models.ForeignKey(
        UserProfil, on_delete=models.CASCADE, related_name="offer_details", null=True, blank=True
    )
    offer = models.ForeignKey(
        Offer, related_name="details", on_delete=models.CASCADE, default=""
    )
    title = models.CharField(max_length=50)
    revisions = models.PositiveIntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField(blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=20, choices=[
        ("basic", "Basic"),
        ("standard", "Standard"),
        ("premium", "Premium")
    ])
    url = models.URLField(blank=True)


class Order(models.Model):
    customer_user = models.ForeignKey(
        UserProfil, on_delete=models.CASCADE, related_name="orders"
    )
    business_user = models.ForeignKey(
        UserProfil, related_name='business_user', on_delete=models.CASCADE, null=True
    )
    offer_detail = models.ForeignKey(
        OfferDetail, on_delete=models.CASCADE, related_name="orders", null=True
    )
    delivery_time_in_days = models.PositiveIntegerField(blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    status = models.CharField(max_length=20, default="in_progress", choices=[
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    business_user = models.ForeignKey(
        UserProfil, on_delete=models.CASCADE, related_name="received_reviews"
    )
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="given_reviews"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BaseInfo(models.Model):
    review_count = models.IntegerField(blank=True)
    average_rating = models.DecimalField(
        max_digits=1, decimal_places=1, blank=True)
    business_profile_count = models.IntegerField(blank=True)
    offer_count = models.IntegerField(blank=True)