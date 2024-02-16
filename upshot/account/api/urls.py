from rest_framework.routers import SimpleRouter
from . import views

app_name = "account-api"
router = SimpleRouter()

router.register("users", views.UserModelViewSet, basename="api-users")
router.register("profiles", views.ProfileModelViewSet, basename="api-profiles")

urlpatterns = [] + router.urls
