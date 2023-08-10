from datetime import datetime

from django.db.models import F, Value, Count
from django.db.models.functions import Concat
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import viewsets

from airport.models import (
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Crew,
    Flight
)

from api.filters.airport_filters import (
    FlightFilter,
    AirportFilter,
    AirplaneFilter
)

from api.permissions import IsAdminOrIfAuthenticatedReadOnly
from api.serializers.airport_serializers import (
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer,
    AirportSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    CrewSerializer,
    FlightSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    CrewDetailSerializer,
)


@extend_schema(tags=["AirplaneTypes"])
class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


@extend_schema(tags=["Airplanes"])
class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneListSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filterset_class = AirplaneFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AirplaneDetailSerializer
        if self.action == "list":
            return AirplaneListSerializer
        return AirplaneSerializer

    def get_queryset(self):
        if self.action in ("retrieve", "list"):
            return Airplane.objects.select_related("airplane_type")
        return Airplane.objects.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "airplane_type",
                type=str,
                description="Filter by airplane_type, lookup=icontains "
                            "(ex.?airplane_type=Airplane1) ",
                required=False
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Airports"])
class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filterset_class = AirportFilter

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "airplane_type",
                type=str,
                description="Filter by closest_big_city, lookup=iexact "
                            "(ex.?closest_big_city=Florida)",
                required=False
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Routes"])
class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RouteDetailSerializer
        if self.action == "list":
            return RouteListSerializer
        return RouteSerializer

    def get_queryset(self):
        if self.action in ("retrieve", "list"):
            return Route.objects.select_related("source", "destination")
        return Route.objects.all()


@extend_schema(tags=["Crews"])
class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return CrewDetailSerializer
        return CrewSerializer

    def get_queryset(self):
        if self.action in ("list", "retrieve"):
            return self.queryset.annotate(
                flights_count=Count("flights")
            )
        return self.queryset


@extend_schema(tags=["Flights"])
class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )
    filterset_class = FlightFilter

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer

    def get_queryset(self):
        if self.action in ("retrieve", "list"):
            return Flight.objects.prefetch_related(
                "crews",
            ).select_related(
                "airplane",
                "route__destination",
                "route__source"
            ).annotate(
                route_full_name=Concat(
                    F("route__source__name"),
                    Value("->"),
                    F("route__destination__name")
                ),
                available_tickets=(
                    F("airplane__seats_in_row") * F("airplane__rows")
                    - Count("tickets")
                )
            )
        return Flight.objects.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "route_destination",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by route->source "
                            "(ex.?route_destination=1,2)",
                required=False
            ),
            OpenApiParameter(
                "departure_time",
                type=datetime,
                description="Filter by departure_time "
                            "(ex.?departure_time=2023-08-09T11:55:00Z)",
                required=False
            ),
            OpenApiParameter(
                "airplane",
                type=int,
                description="Filter by airplane (ex.?airplane=1)",
                required=False
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
