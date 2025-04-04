from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfil(models.Model):
    CATEGORY_CHOICES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    type = models.CharField(
        max_length=10, choices=CATEGORY_CHOICES, null=False, blank=False)
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    file = models.FileField(max_length=99, blank=True, upload_to='images/')
    location = models.CharField(max_length=25, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=255, blank=True)
    working_hours = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)


class Offer(models.Model):
    user = models.ForeignKey(
        UserProfil, on_delete=models.CASCADE, related_name='offers'
    )
    title = models.CharField(max_length=50)
    image = models.FileField(max_length=99, blank=True, null=True, upload_to='images/')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    min_delivery_time = models.PositiveIntegerField(blank=True, null=True)


class OfferDetail(models.Model):
    business_user = models.ForeignKey(
        UserProfil, on_delete=models.CASCADE, related_name='offer_details', null=True, blank=True
    )
    offer = models.ForeignKey(
        Offer, related_name='details', on_delete=models.CASCADE, default=""
    )
    title = models.CharField(max_length=50)
    revisions = models.PositiveIntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField(blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=20, choices=[
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium')
    ])
    url = models.URLField(blank=True)


class Order(models.Model):
    customer_user = models.ForeignKey(
        UserProfil, on_delete=models.CASCADE, related_name='orders'
    )
    business_user = models.ForeignKey(
        UserProfil, related_name='business_user', on_delete=models.CASCADE, null=True
    )
    offer_detail = models.ForeignKey(
        OfferDetail, on_delete=models.CASCADE, related_name='orders', null=True
    )
    delivery_time_in_days = models.PositiveIntegerField(blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    status = models.CharField(max_length=20, default='in_progress', choices=[
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    business_user = models.ForeignKey(
        UserProfil, on_delete=models.CASCADE, related_name='received_reviews'
    )
    reviewer = models.ForeignKey(
        UserProfil, on_delete=models.CASCADE, related_name='given_reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)