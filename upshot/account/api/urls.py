from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views as jwt_views
from django.urls import path
from . import views

app_name = "account-api"
router = SimpleRouter()

router.register("users", views.UserModelViewSet, basename="api-users")
router.register("profiles", views.ProfileModelViewSet, basename="api-profiles")
router.register("contacts", views.ContactModelViewSet, basename="api-contacts")

urlpatterns = [
    # JWT create
    path(
        "jwt/create/",
        jwt_views.TokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    # JWT refresh
    path(
        "jwt/refresh/", jwt_views.TokenRefreshView.as_view(), name="jwt-refresh"
    ),
    # TOKEN
    path(
        "token/create/",
        jwt_views.TokenObtainSlidingView.as_view(),
        name="token-create",
    ),
    path(
        "token/refresh/",
        jwt_views.TokenRefreshSlidingView.as_view(),
        name="token-refresh",
    ),
    path(
        "token/verify/",
        jwt_views.TokenVerifyView.as_view(),
        name="token-verify",
    ),
    # blacklist
    path(
        "jwt/blacklist/",
        views.JWTTokenBlacklistView.as_view(),
        name="jwt-blacklist",
    ),
    path(
        "token/blacklist/",
        views.SlidingTokenBlacklistView.as_view(),
        name="token-blacklist",
    ),
] + router.urls
