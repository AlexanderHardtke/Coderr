from django.contrib import admin
from django.urls import path, include
from .views import UserListViewSet
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

# router = routers.SimpleRouter()
# router.register(r'offers', UserListViewSet)
# router.register(r'orders', UserListViewSet)
# router.register(r'reviews', UserListViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('registration/', UserListViewSet.as_view(), name='registration-detail'),
    path('login/', UserListViewSet.as_view(), name='login'),
    path('profile/<int:pk>/', UserListViewSet.as_view(), name='profile-detail'),
    path('profiles/business/', UserListViewSet.as_view(), name='profiles-list'),
    path('profiles/customer/', UserListViewSet.as_view(), name='profiles-list'),
    # path/('/base-info/')
]