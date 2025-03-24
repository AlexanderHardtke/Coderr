from rest_framework import views, generics, status, filters, viewsets, mixins, serializers
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
    Reviewserializer, BaseInfoSerializer, OfferDetailSerializer
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


class OfferViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    # pagination_class = SmallResultSetPagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['creator_id', 'min_price', 'max_delivery_time', 'ordering', 'search', 'page_size']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user.userprofil 
        permission_classes = [IsBusinessUser]
        serializer.save(user=user)

    def patch():
        permission_classes = [IsOwnerOrAdmin]

    def delete():
        permission_classes = [IsOwnerOrAdmin]


class OfferDetailView(APIView):
    permission_classes = [AllowAny]
    queryset = OfferDetail.objects.all()

    def get(self, request, pk, format=None):
        try:
            offer = OfferDetail.objects.get(pk=pk)
            serializer = OfferDetailSerializer(offer)
            return Response(serializer.data)
        except Offer.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post():
        permission_classes = [IsCustomerUser]

    def patch():
        permission_classes = [IsOwnerOrAdmin]

    def delete():
        permission_classes = [IsOwnerOrAdmin]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = Reviewserializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id', 'ordering']
    ordering_fields = ['updated_at', 'rating']
    ordering = ['rating']

    def post():
        permission_classes = [IsCustomerUser]

    def patch():
        permission_classes = [IsOwnerOrAdmin]

    def delete():
        permission_classes = [IsOwnerOrAdmin]


class BaseInfoView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = BaseInfo.objects.all()
    serializer_class = BaseInfoSerializer
