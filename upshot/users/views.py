from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreationForm

User = get_user_model()


class UserCreateView(LoginRequiredMixin, CreateView):
    form_class = UserCreationForm
    http_method_names = ["get", "post"]

    model = User
    template_name = "users/create.html"

    def get_success_url(self):
        url = reverse(
            "profiles:profile-edit", kwargs={"username": self.object.username}
        )
        return url


class UserRegisterView(CreateView):
    form_class = UserCreationForm
    http_method_names = ["get", "post"]

    model = User
    template_name = "users/register.html"

    def get_success_url(self):
        url = reverse(
            "profiles:profile-edit", kwargs={"username": self.object.username}
        )
        return url
