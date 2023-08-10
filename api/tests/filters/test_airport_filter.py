from django.utils import timezone

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory

from airport.models import Airport, Airplane, AirplaneType, Flight, Route


class BaseMixin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            email="user@gmail.com",
            password="password123e"
        )
        self.client.force_authenticate(self.user)


def sample_airport(quantity):
    for i in range(quantity):
        airport = Airport.objects.create(
            name=f"Airport{i}",
            closest_big_city=f"City{i}",

        )
    return airport


def sample_airplane(quantity):
    airplane = None
    for i in range(quantity):
        airplane_type, _ = AirplaneType.objects.get_or_create(
            name=f"Type{i}"
        )
        airplane = Airplane.objects.create(
            name=f"Airplane{i}",
            rows=i,
            seats_in_row=i,
            airplane_type=airplane_type
        )
    return airplane


def sample_flight(additional):
    route = Route.objects.create(
        source=sample_airport(additional),
        destination=sample_airport(additional),
        distance=additional*1000
    )
    airplane = sample_airplane(additional)
    departure_time = timezone.now()
    arrival_time = timezone.now() + timezone.timedelta(days=additional)

    flight = Flight.objects.create(
        route=route,
        airplane=airplane,
        departure_time=departure_time,
        arrival_time=arrival_time
    )
    return flight


class TestAirportFilter(BaseMixin):
    def setUp(self):
        super().setUp()
        self.url = reverse("api:airport-list")

    def test_closest_by_city(self):
        airport = sample_airport(3)

        response = self.client.get(
            self.url,
            {
                "closest_big_city": airport.closest_big_city
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.data["results"]))
        self.assertEqual(
            airport.closest_big_city,
            response.data["results"][0]["closest_big_city"]
        )


class TestAirPlaneFilter(BaseMixin):
    def setUp(self):
        super().setUp()
        self.url = reverse("api:airplane-list")

    def test_airplane_type_name(self):
        airplane = sample_airplane(3)

        response = self.client.get(
            self.url,
            {
                "airplane_type": airplane.airplane_type.name
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.data["results"]))
        self.assertEqual(
            airplane.name,
            response.data["results"][0]["name"]
        )


class TestFlightFilter(BaseMixin):
    def setUp(self):
        super().setUp()
        self.url = reverse("api:flight-list")

    def test_route_destination(self):
        flight1 = sample_flight(1)
        flight2 = sample_flight(2)

        response = self.client.get(
            self.url,
            {
                "route_destination": {
                    f"{flight1.route.source.id}, {flight1.route.destination.id}"
                }
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.data["results"]))
        self.assertEqual(
            f"{flight1.route.source.name}->{flight1.route.destination.name}",
            response.data["results"][0]["route_full_name"]
        )
        self.assertNotEquals(
            f"{flight2.route.source.name}->{flight2.route.destination.name}",
            response.data["results"][0]["route_full_name"]
        )

    def test_departure_time(self):
        flight1 = sample_flight(1)
        flight2 = sample_flight(2)
        departure = flight1.departure_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        response = self.client.get(
            self.url,
            {
                "departure_time": departure
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.data["results"]))
        self.assertEqual(
            departure,
            response.data["results"][0]["departure_time"]
        )
        self.assertNotEquals(
            flight2.departure_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            response.data["results"][0]["departure_time"]
        )

    def test_airplane_test(self):
        flight1 = sample_flight(1)
        flight2 = sample_flight(2)

        response = self.client.get(
            self.url,
            {
                "airplane": flight1.airplane.id
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.data["results"]))

        self.assertEqual(
            flight1.airplane.name,
            response.data["results"][0]["airplane"]
        )
        self.assertNotEquals(
            flight2.airplane.name,
            response.data["results"][0]["airplane"]
        )
