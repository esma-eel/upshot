from rest_framework.routers import SimpleRouter
from . import views

app_name = "article-api"
router = SimpleRouter()

router.register("", views.ArticleModelViewSet, basename="api-articles")
router.register("comments", views.CommentModelViewSet, basename="api-comments")

urlpatterns = [] + router.urls
