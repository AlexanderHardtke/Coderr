from rest_framework import views, generics
from coderr_db.models import BusinessUserProfile, CustomerUserProfile
from .serializers import BusinessUserProfileSerializer, CustomerUserProfileSerializer
from rest_framework.permissions import AllowAny


class BusinessUserList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = BusinessUserProfile.objects.all()
    serializer_class = BusinessUserProfileSerializer