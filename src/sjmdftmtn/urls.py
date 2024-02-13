from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from article.views import home_view, search_objects

urlpatterns = [
    # mtv
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("article/", include("article.urls", namespace="article")),
    path("search/", search_objects, name="search_objects"),
    # api
    path("api/article/", include("article.api.urls", namespace="api-article")),
    # home
    path("", home_view, name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
