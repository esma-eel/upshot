from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path(
        r"<str:username>/",
        views.ProfileView.as_view(),
        name="profile",
    ),
    path(
        r"<str:username>/edit/",
        views.ProfileEditView.as_view(),
        name="profile-edit",
    ),
]
