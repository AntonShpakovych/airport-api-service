from rest_framework import mixins, viewsets

from cart.models import Order

from api.permissions import IsAdminOrIfAuthenticatedReadOnly
from api.serializers.cart_serializers import (
    OrderSerializer,
    OrderListSerializer
)


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).prefetch_related(
            "tickets__flight__airplane",
            "tickets__flight__crews"
        )

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
