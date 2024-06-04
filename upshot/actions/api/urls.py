from rest_framework.routers import SimpleRouter
from . import views

app_name = "actions-api"
router = SimpleRouter()

router.register("", views.ActionModelViewSet, basename="api-action")

urlpatterns = [] + router.urls
