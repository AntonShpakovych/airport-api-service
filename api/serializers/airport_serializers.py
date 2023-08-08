from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from airport.models import (
    AirplaneType,
    Airplane,
    Route,
    Airport
)


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


class AirplaneSerializerList(AirplaneSerializer):
    airplane_type = serializers.CharField(
        source="airplane_type.name",
        read_only=True
    )


class AirplaneSerializerDetail(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(many=False, read_only=True)

    class Meta(AirplaneSerializerList.Meta):
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


class RouteSerializerList(RouteSerializer):
    source = serializers.CharField(
        source="source.name",
        read_only=True
    )
    destination = serializers.CharField(
        source="destination.name",
        read_only=True
    )


class RouteSerializerDetail(RouteSerializer):
    source = AirportSerializer(many=False, read_only=True)
    destination = AirportSerializer(many=False, read_only=True)
