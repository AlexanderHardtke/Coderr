from django.contrib import admin
from django.urls import path, include
from .views import RegistrationView, UserListBusinessViewSet, UserListCustomerViewSet, LoginView, UserSingleView
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

# router = routers.SimpleRouter()
# router.register(r'offers', UserListViewSet)
# router.register(r'orders', UserListViewSet)
# router.register(r'reviews', UserListViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('registration/', RegistrationView.as_view(), name='registration-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:pk>/', UserSingleView.as_view(), name='profile-detail'),
    path('profiles/business/', UserListBusinessViewSet.as_view(), name='profiles-business-list'),
    path('profiles/customer/', UserListCustomerViewSet.as_view(), name='profiles-customer-list'),
    # path/('/base-info/')
]