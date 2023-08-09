from django.urls import path, include

from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from api.views.account_views import (
    CreateUserView,
    ManageUserView
)
from api.views.airport_views import (
    AirplaneTypeViewSet,
    AirplaneViewSet,
    AirportViewSet,
    RouteViewSet,
    CrewViewSet,
    FlightViewSet,
)
from api.views.cart_views import (
    OrderViewSet
)


router_airport = routers.DefaultRouter()
router_cart = routers.DefaultRouter()

router_airport.register("airplane_types", AirplaneTypeViewSet)
router_airport.register("airplanes", AirplaneViewSet)
router_airport.register("airports", AirportViewSet)
router_airport.register("routes", RouteViewSet)
router_airport.register("crews", CrewViewSet)
router_airport.register("flights", FlightViewSet)

router_cart.register("orders", OrderViewSet)

urlpatterns = [
    path(
        "account/register/",
        CreateUserView.as_view(),
        name="create"
    ),
    path(
        "account/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),
    path(
        "account/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
    path(
        "account/token/verify/",
        TokenVerifyView.as_view(),
        name="token_verify"
    ),
    path(
        "account/profile/",
        ManageUserView.as_view(),
        name="profile"
    ),
    path(
        "airport/",
        include(router_airport.urls)
    ),
    path(
        "cart/",
        include(router_cart.urls)
    )
]

app_name = "api"
