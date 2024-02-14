from rest_framework.routers import SimpleRouter
from . import views

app_name = "article-api"
router = SimpleRouter()

router.register("comments", views.CommentModelViewSet, basename="api-comments")
router.register("", views.ArticleModelViewSet, basename="api-articles")

urlpatterns = [] + router.urls
