from django.contrib import admin
from django.urls import path, include
from .views import (
    RegistrationView, UserListBusinessView, UserListCustomerView,
    LoginView, UserSingleView, OrderViewSet, OfferViewSet, ReviewViewSet, BaseInfoView
    )
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.SimpleRouter()
router.register(r'offers', OfferViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('registration/', RegistrationView.as_view(), name='registration-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:pk>/', UserSingleView.as_view(), name='profile-detail'),
    path('profiles/business/', UserListBusinessView.as_view(), name='profiles-business-list'),
    path('profiles/customer/', UserListCustomerView.as_view(), name='profiles-customer-list'),
    path('base-info/', BaseInfoView.as_view(), name='base-info-list')
]