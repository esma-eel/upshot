from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from upshot.article.views import search_objects, home_view


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)


media_url = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
static_url = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns = [
    # mtv
    path("admin/", admin.site.urls),
    path("account/", include("upshot.account.urls")),
    path("article/", include("upshot.article.urls", namespace="article")),
    path("search/", search_objects, name="search_objects"),
    # api
    path(
        "api/article/",
        include("upshot.article.api.urls", namespace="api-article"),
    ),
    path(
        "api/mentor/", include("upshot.mentor.api.urls", namespace="api-mentor")
    ),
    # home
    path("", home_view, name="home"),
    # swagger
    path(
        "swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

if bool(settings.DEBUG):
    urlpatterns = urlpatterns + media_url
    urlpatterns = urlpatterns + static_url
