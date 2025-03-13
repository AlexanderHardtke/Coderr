from rest_framework import views, generics
from coderr_db.models import UserProfil
from .serializers import UserProfilSerializer
from rest_framework.permissions import AllowAny


class UserListViewSet(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = UserProfil.objects.all()
    serializer_class = UserProfilSerializer