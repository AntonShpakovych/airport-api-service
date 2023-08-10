import django_filters
from django_filters import (
    BaseRangeFilter,
    DateTimeFilter,
    CharFilter
)

from airport.models import Flight


class FlightFilter(django_filters.FilterSet):
    route_destination = BaseRangeFilter(method="route_filter")
    departure_time = DateTimeFilter(
        field_name="departure_time",
        lookup_expr="exact"
    )

    class Meta:
        model = Flight
        fields = ["airplane"]

    def route_filter(self, queryset, name, value):
        source, destination = value

        return queryset.filter(
            route__source_id=source,
            route__destination_id=destination
        )


class AirportFilter(django_filters.FilterSet):
    closest_big_city = CharFilter(
        field_name="closest_big_city",
        lookup_expr="iexact"
    )


class AirplaneFilter(django_filters.FilterSet):
    airplane_type = CharFilter(
        field_name="airplane_type__name",
        lookup_expr="icontains"
    )
