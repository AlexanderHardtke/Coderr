from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class UserProfil(models.Model):
    CATEGORY_CHOICES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    type = models.CharField(
        max_length=10, choices=CATEGORY_CHOICES, default='customer')
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
    user = models.OneToOneField(
        UserProfil, on_delete=models.CASCADE, unique=True
    )
    title = models.CharField(max_length=50)
    image = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    details = models.ForeignKey()


class OfferDetail(models.Model):
    offer = models.ForeignKey(
        Offer, related_name="details", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50)
    revisions = models.PositiveIntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField(
        blank=False, max_length=3
    )
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=20, choices=[
        ("basic", "Basic"),
        ("standard", "Standard"),
        ("premium", "Premium")
    ])
    url = models.URLField()


class Order(models.Model):
    customer_user = models.ForeignKey(
        User, related_name="orders", on_delete=models.CASCADE
    )
    business_user = models.ForeignKey(
        User, related_name="offers", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50)
    revisions = models.PositiveIntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField(blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=20, default="basic", choices=[
        ("basic", "Basic"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    ])
    status = models.CharField(max_length=20, default="in_progress", choices=[
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    business_user = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        max_digits=1, max_value=5, min_value=1, blank=False
    )
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BaseInfo(models.Model):
    review_count = models.IntegerField(max_length=4, blank=True)
    average_rating = models.DecimalField(
        max_digits=1, decimal_places=1, max_value=5, min_value=1, blank=True)
    business_profile_count = models.IntegerField(max_length=4, blank=True)
    offer_count = models.IntegerField(max_length=4, blank=True)
