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
    RouteViewSet
)


router = routers.DefaultRouter()

router.register("airplane_types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)

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
    path("airport/", include(router.urls))

]

app_name = "api"
