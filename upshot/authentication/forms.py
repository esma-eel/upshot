from django import forms
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from django.contrib.auth import authenticate, get_user_model
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from upshot.common.utils.generators import default_token_generator
from upshot.profiles.models import ProfileEmail, ProfilePhoneNumber
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class PasswordResetFormEmailChecker(PasswordResetForm):
    def clean_email(self):
        to_email = self.cleaned_data.get("email")
        query_set = ProfileEmail.objects.filter(
            email=to_email, is_verified=True, is_primary=True
        )

        if not query_set.exists():
            raise forms.ValidationError("Verified Primary Email not found!")

        return to_email

    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override

        qs = ProfileEmail.objects.filter(
            email=email, is_verified=True, is_primary=True
        )

        if qs.exists():
            profile_email_object = qs.last()
            profile_object = profile_email_object.profile
            user = profile_object.user
            context = {
                "email": email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": default_token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                email,
                html_email_template_name=html_email_template_name,
            )


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"autofocus": True})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "Please enter correct credentials. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = None

        if username is not None and password:
            phone_qs = ProfilePhoneNumber.objects.filter(
                phone_number=username, is_primary=True, is_active=True
            )
            email_qs = ProfileEmail.objects.filter(
                email=username, is_primary=True, is_active=True
            )

            user_qs = User.objects.filter(username=username)

            if phone_qs.exists():
                user = phone_qs.last().profile.user
            elif email_qs.exists():
                user = email_qs.last().profile.user
            elif user_qs.exists():
                user = user_qs.last()

            if user:
                username = user.username

            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
