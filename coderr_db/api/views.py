from rest_framework import generics, status, filters, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import SmallResultSetPagination
from .permissions import IsOwnerOrAdmin, IsBusinessUser, IsCustomerUser, IsOwnerOrAdminOfReview, IsOwnerOrAdminOfOrder
from coderr_db.models import UserProfil, Order, Offer, OfferDetail, Review
from .serializers import (
    UserProfilSerializer, RegistrationSerializer, UserProfilBusinessSerializer,
    UserProfilCustomerSerializer, OfferSerializer, OrderSerializer,
    Reviewserializer, OfferDetailSerializer, OfferGetSerializer, OrderCountSerializer
)
from django.db.models import Avg, Count


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
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['details__updated_at', 'details__price']
    allowed_query_params = {
        'creator_id', 'min_price',
        'max_delivery_time', 'search', 'ordering'
    }

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsBusinessUser()]
        else:
            return [IsOwnerOrAdmin()]

    def list(self, request):
        self.pagination_class = SmallResultSetPagination
        query_params = set(request.query_params.keys())
        invalid_params = query_params - self.allowed_query_params
        if invalid_params:
            return Response(
                {"error": "Ungültige Anfrageparameter."},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        serializer = OfferGetSerializer(
            page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = OfferGetSerializer(queryset, context={'request': request})
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

        delivery_param = self.request.query_params.get(
            'max_delivery_time', None)
        if delivery_param is not None:
            queryset = queryset.filter(
                details__delivery_time_in_days__lte=delivery_param)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user.userprofil
        serializer.save(user=user)


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

    def create(self, request, *args, **kwargs):
        if not IsCustomerUser().has_permission(request, self):
            return Response(
                {'detail': 'Nur Kunden dürfen Bestellungen erstellen.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if "status" not in request.data or len(request.data) > 1:
            return Response(
                {"error": "Ungültiger Status oder unzulässige Felder in der Anfrage."},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance = self.get_object()
        if not IsOwnerOrAdminOfOrder().has_permission(request, self, instance):
            return Response(
                {'detail': 'Nur der zuständige Anbieter darf die Bestellungen bearbeiten.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().partial_update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return Response({"error": "Detailansicht nicht erlaubt."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"error": "Benutzer hat keine Berechtigung, die Bestellung zu löschen."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class OrderCountBaseView(generics.RetrieveAPIView):
    serializer_class = OrderCountSerializer
    queryset = Order.objects.all()

    def get_object(self):
        return {
            "order_count": self.get_queryset().filter(
                business_user=self.kwargs["pk"]
            ).count()
        }


class OrderCountView(OrderCountBaseView):
    def get_queryset(self):
        return super().get_queryset().filter(status='in_progress')


class CompletedOrderCountView(OrderCountBaseView):
    def get_queryset(self):
        return super().get_queryset().filter(status='completed')


class ReviewViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
):
    queryset = Review.objects.all()
    serializer_class = Reviewserializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['updated_at', 'rating']
    ordering = ['updated_at']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        if self.request.method == 'POST':
            return [IsCustomerUser()]
        else:
            return [IsOwnerOrAdminOfReview()]

    def get_queryset(self):
        queryset = super().get_queryset()
        business_user_id = self.request.query_params.get(
            "business_user_id", None)
        reviewer_id = self.request.query_params.get("reviewer_id", None)

        if business_user_id:
            queryset = queryset.filter(business_user=business_user_id)
        if reviewer_id:
            queryset = queryset.filter(reviewer=reviewer_id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        if not IsCustomerUser().has_permission(request, self):
            return Response(
                {'detail': 'Nur Kunden dürfen Bewertungen erstellen.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if 'rating' not in request.data:
            return Response(
                {"error": "Fehlerhafte Anfrage, Rating fehlt."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        return super().destroy(request, *args, **kwargs)


class BaseInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        review_stats = Review.objects.aggregate(
            review_count=Count('id'),
            average_rating=Avg('rating'),
        )
        business_count = UserProfil.objects.filter(type='business').count()
        offer_count = Offer.objects.count()

        data = {
            "review_count": review_stats['review_count'],
            "average_rating": round(float(review_stats['average_rating'] or 0), 1),
            "business_profile_count": business_count,
            "offer_count": offer_count
        }

        return Response(data)
