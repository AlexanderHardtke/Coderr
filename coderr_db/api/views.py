from rest_framework import views, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

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
            data=serializer.errors

        return Response({"your message": data}, status=status.HTTP_201_CREATED)



class UserListBusinessViewSet(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = UserProfil.objects.filter(type='business')
    serializer_class = UserProfilSerializer


class UserListCustomerViewSet(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = UserProfil.objects.filter(type='customer')
    serializer_class = UserProfilSerializer