from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory

from api.tests.filters.test_airport_filter import sample_flight
from cart.models import Order, Ticket


def sample_order(user, additional):
    order = Order.objects.create(
        user=user
    )

    Ticket.objects.create(
        row=additional,
        seat=additional,
        flight=sample_flight(additional+1),
        order=order
    )
    return order


class CartFilter(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            email="user@gmail.com",
            password="password123e"
        )
        self.client.force_authenticate(self.user)
        self.url = reverse("api:order-list")

    def test_created_at(self):
        order = sample_order(self.user, 1)

        response = self.client.get(
            self.url,
            {
                "created_at": order.created_at
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.data["results"]))
        self.assertEqual(
            order.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            response.data["results"][0]["created_at"]
        )
