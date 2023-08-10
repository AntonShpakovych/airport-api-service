from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from cart.models import Order

from api.permissions import IsAdminOrIfAuthenticatedReadOnly
from api.serializers.cart_serializers import (
    OrderSerializer,
    OrderListSerializer
)


@extend_schema(tags=["Carts"])
class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user).prefetch_related(
            "tickets__flight__airplane",
            "tickets__flight__crews"
        )

        created_at = self.request.query_params.get("created_at")

        if created_at:
            queryset = queryset.filter(created_at=created_at)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
