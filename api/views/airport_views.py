from rest_framework import viewsets

from airport.models import (
    AirplaneType,
    Airplane,
    Airport,
    Route
)

from api.permissions import IsAdminOrIfAuthenticatedReadOnly
from api.serializers.airport_serializers import (
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirplaneSerializerList,
    AirplaneSerializerDetail,
    AirportSerializer,
    RouteSerializer,
    RouteSerializerList,
    RouteSerializerDetail
)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializerList
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AirplaneSerializerDetail
        if self.action == "list":
            return AirplaneSerializerList
        return AirplaneSerializer

    def get_queryset(self):
        if self.action in ("retrieve", "list"):
            return Airplane.objects.select_related("airplane_type")
        return Airplane.objects.all()


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RouteSerializerDetail
        if self.action == "list":
            return RouteSerializerList
        return RouteSerializer

    def get_queryset(self):
        if self.action in ("retrieve", "list"):
            return Route.objects.select_related("source", "destination")
        return Route.objects.all()
