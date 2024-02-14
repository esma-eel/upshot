from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from upshot.common.utils.generators import default_token_generator
from .forms import PasswordResetFormEmailChecker, LoginForm

# Create your views here.


class PasswordChangeView(auth_views.PasswordChangeView):
    success_url = reverse_lazy("authentication:password-change-done")


class PasswordResetView(auth_views.PasswordResetView):
    form_class = PasswordResetFormEmailChecker
    success_url = reverse_lazy("authentication:password-reset-done")


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy("authentication:password-reset-complete")
    token_generator = default_token_generator


class LoginView(auth_views.LoginView):
    redirect_authenticated_user = True
    authentication_form = LoginForm
