from django.contrib import admin
from django.urls import path, include
from .views import (
    RegistrationView, UserListBusinessView, UserListCustomerView,
    LoginView, UserSingleView, OrderViewSet, OfferViewSet, ReviewViewSet,
    BaseInfoView, OfferDetailView, OrderCountView, CompletedOrderCountView
    )
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.SimpleRouter()
router.register(r'offers', OfferViewSet, basename='offers')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('registration/', RegistrationView.as_view(), name='registration-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:pk>/', UserSingleView.as_view(), name='profile-detail'),
    path('profiles/business/', UserListBusinessView.as_view(), name='profiles-business-list'),
    path('profiles/customer/', UserListCustomerView.as_view(), name='profiles-customer-list'),
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name='offerdetails-detail'),
    path('order-count/<int:pk>/', OrderCountView.as_view(), name='order-count-detail'),
    path('completed-order-count/<int:pk>/', CompletedOrderCountView.as_view(), name='completed-order-count-detail'),
    path('base-info/', BaseInfoView.as_view(), name='base-info-list')
]