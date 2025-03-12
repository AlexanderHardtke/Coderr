from django.contrib import admin
from django.urls import path, include
from .views import ContactViewSet, ProfilesBusinessList, ProfilesBusinessDetail, ProfileCustomer, OrderViewSet, RegistrationView, UserLogin
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.SimpleRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/', ProfilesBusinessList.as_view(), name='users-list'),
    path('user/<int:pk>/', ProfilesBusinessDetail.as_view(), name='user-detail'),
    path('registration/', RegistrationView.as_view(), name='registration-detail'),
    path('login/', UserLogin.as_view(), name='login'),
    path('usercheck/', CheckUserList.as_view(), name='usercheck-list')
]