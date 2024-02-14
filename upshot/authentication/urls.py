from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
    LoginView,
)

app_name = "authentication"

urlpatterns = [
    path(
        "password-change/",
        PasswordChangeView.as_view(),
        name="password-change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password-change-done",
    ),
    path(
        "password-reset/",
        PasswordResetView.as_view(),
        name="password-reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password-reset-done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password-reset-complete",
    ),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
