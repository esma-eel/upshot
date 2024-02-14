from rest_framework.routers import SimpleRouter
from . import views

app_name = "mentor-api"
router = SimpleRouter()

router.register(
    "settings",
    views.MentorSettingModelViewSet,
    basename="api-mentor-settings",
)
router.register(
    "requests",
    views.MentorRequestModelViewSet,
    basename="api-mentor-requests",
)

urlpatterns = [] + router.urls
