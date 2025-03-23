from rest_framework import views, generics, status, filters
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django_filters.rest_framework import DjangoFilterBackend

from .pagination import SmallResultSetPagination
from .permissions import IsOwnerOrAdmin, IsBusinessUser, IsCustomerUser
from coderr_db.models import UserProfil, Order, Offer, OfferDetail, Review, BaseInfo
from .serializers import (
    UserProfilSerializer, RegistrationSerializer, UserProfilBusinessSerializer,
    UserProfilCustomerSerializer, OfferSerializer, OrderSerializer,
    Reviewserializer, BaseInfoSerializer
)


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_user = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_user)
            data = {
                'token': token.key,
                'username': saved_user.username,
                'email': saved_user.email,
                'user_id': saved_user.pk,
            }
        else:
            Response({"your message": serializer.errors},
                     status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)


class UserListBusinessView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = UserProfil.objects.filter(type='business')
    serializer_class = UserProfilBusinessSerializer


class UserListCustomerView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = UserProfil.objects.filter(type='customer')
    serializer_class = UserProfilCustomerSerializer


class UserSingleView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = UserProfil.objects.all()
    serializer_class = UserProfilSerializer


class OfferViewSet(generics.GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    pagination_class = SmallResultSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['creator_id', 'min_price', 'max_delivery_time', 'ordering', 'search', 'page_size']

    def post():
        permission_classes = [IsCustomerUser]
        pass

    def patch():
        permission_classes = [IsOwnerOrAdmin]
        pass

    def delete():
        permission_classes = [IsOwnerOrAdmin]
        pass


class OrderViewSet():
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post():
        permission_classes = [IsBusinessUser]
        pass

    def patch():
        permission_classes = [IsOwnerOrAdmin]
        pass

    def delete():
        permission_classes = [IsOwnerOrAdmin]
        pass


class ReviewViewSet():
    queryset = Review.objects.all()
    serializer_class = Reviewserializer

    def post():
        permission_classes = [IsCustomerUser]
        pass

    def patch():
        permission_classes = [IsOwnerOrAdmin]
        pass

    def delete():
        permission_classes = [IsOwnerOrAdmin]
        pass
 


class BaseInfoView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = BaseInfo.objects.all()
    serializer_class = BaseInfoSerializer
