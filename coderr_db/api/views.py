from rest_framework import views, generics, status, filters, viewsets, mixins, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
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
    Reviewserializer, BaseInfoSerializer, OfferDetailSerializer, OfferListSerializer
)


class RegistrationView(APIView):

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
    queryset = UserProfil.objects.filter(type='business')
    serializer_class = UserProfilBusinessSerializer


class UserListCustomerView(generics.ListAPIView):
    queryset = UserProfil.objects.filter(type='customer')
    serializer_class = UserProfilCustomerSerializer


class UserSingleView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = UserProfil.objects.all()
    serializer_class = UserProfilSerializer


class OfferViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    # pagination_class = SmallResultSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['details__updated_at', 'details__price']
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = OfferListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()

        creator_param = self.request.query_params.get('creator_id', None)
        if creator_param is not None:
            queryset = queryset.filter(user__id=creator_param)

        price_param = self.request.query_params.get('min_price', None)
        if price_param is not None:
            price_param = float(price_param)
            queryset = queryset.filter(details__price__lte=price_param)

        delivery_param = self.request.query_params.get('max_delivery_time', None)
        if delivery_param is not None:
            queryset = queryset.filter(details__delivery_time_in_days__lte=delivery_param)

        return queryset
    
    def perform_create(self, serializer):
        user = self.request.user.userprofil 
        permission_classes = [IsBusinessUser]
        serializer.save(user=user)

    def patch():
        permission_classes = [IsOwnerOrAdmin]

    def delete():
        permission_classes = [IsOwnerOrAdmin]


class OfferDetailView(APIView):
    queryset = OfferDetail.objects.all()

    def get(self, request, pk, format=None):
        if not request.user.is_authenticated:
            return Response({'detail': 'Benutzer ist nicht authentifiziert'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            permission_classes = [IsAuthenticated]
            offer = OfferDetail.objects.get(pk=pk)
            serializer = OfferDetailSerializer(offer)
            return Response(serializer.data)
        except OfferDetail.DoesNotExist:
            return Response({'detail': 'Das Angebotsdetail mit der angegebenen ID wurde nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': 'Interner Serverfehler.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
