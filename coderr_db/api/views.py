from rest_framework import views, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .permissions import isOwnerOrAdmin
from coderr_db.models import UserProfil
from .serializers import UserProfilSerializer, RegistrationSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_user = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_user)
            data = {
                'token':token.key,
                'username':saved_user.username,
                'email':saved_user.email,
                'user_id':saved_user.pk,
            }
        else:
            Response({"your message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.pk,
            }
        else:
            Response({"your message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_201_CREATED)


class UserListBusinessViewSet(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = UserProfil.objects.filter(type='business')
    serializer_class = UserProfilSerializer


class UserListCustomerViewSet(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = UserProfil.objects.filter(type='customer')
    serializer_class = UserProfilSerializer


class UserSingleView(generics.RetrieveUpdateAPIView):
    queryset = UserProfil.objects.all()
    serializer_class = UserProfilSerializer
    permission_classes = [isOwnerOrAdmin]