from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("create/", views.UserCreateView.as_view(), name="user-create"),
    path("register/", views.UserRegisterView.as_view(), name="user-register"),
]
