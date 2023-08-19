from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from airport.models import (
    AirplaneType,
    Airplane,
    Route,
    Airport,
    Crew,
    Flight
)

from cart.models import Ticket


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ["id", "name"]


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = [
            "id",
            "name",
            "rows",
            "seats_in_row",
            "airplane_type"
        ]


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.CharField(
        source="airplane_type.name",
        read_only=True
    )


class AirplaneDetailSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(
        many=False,
        read_only=True
    )

    class Meta(AirplaneListSerializer.Meta):
        fields = AirplaneSerializer.Meta.fields + ["capacity"]


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = [
            "id",
            "name",
            "closest_big_city"
        ]


class RouteSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super().validate(attrs=attrs)
        Route.validate_source_destination(
            attrs["source"],
            attrs["destination"],
            ValidationError
        )
        return data

    class Meta:
        model = Route
        fields = [
            "id",
            "source",
            "destination",
            "distance"
        ]


class RouteListSerializer(RouteSerializer):
    source = serializers.CharField(
        source="source.name",
        read_only=True
    )
    destination = serializers.CharField(
        source="destination.name",
        read_only=True
    )


class RouteDetailSerializer(RouteSerializer):
    source = AirportSerializer(
        many=False,
        read_only=True
    )
    destination = AirportSerializer(
        many=False,
        read_only=True
    )


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = [
            "id",
            "first_name",
            "last_name"
        ]


class CrewDetailSerializer(CrewSerializer):
    flights_count = serializers.IntegerField()

    class Meta(CrewSerializer.Meta):
        fields = CrewSerializer.Meta.fields + ["flights_count"]


class FlightTakenPlaces(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["row", "seat"]


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = [
            "id",
            "route",
            "airplane",
            "crews",
            "departure_time",
            "arrival_time"
        ]


class FlightListSerializer(serializers.ModelSerializer):
    route_full_name = serializers.CharField(read_only=True)
    available_tickets = serializers.IntegerField(read_only=True)
    airplane = serializers.CharField(
        source="airplane.name",
        read_only=True
    )
    crews = serializers.StringRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = Flight
        fields = [
            "id",
            "airplane",
            "crews",
            "departure_time",
            "arrival_time",
            "route_full_name",
            "available_tickets"
        ]


class FlightDetailSerializer(FlightSerializer):
    route = RouteDetailSerializer(
        many=False,
        read_only=True
    )
    airplane = AirplaneDetailSerializer(
        many=False,
        read_only=True
    )
    crews = CrewSerializer(
        many=True,
        read_only=True
    )
    taken_places = FlightTakenPlaces(
        source="tickets",
        many=True,
        read_only=True
    )

    class Meta(FlightSerializer.Meta):
        fields = FlightSerializer.Meta.fields + ["taken_places"]
