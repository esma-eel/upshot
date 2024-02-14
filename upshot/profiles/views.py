from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import (
    ProfileModelForm,
    ProfilePhoneNumberInlineFormSet,
    ProfileEmailInlineFormSet,
    ProfileAddressInlineFormSet,
)


# Create your views here.
def profile_home(request, username=None):
    return render(
        request,
        template_name="profiles/profile.html",
    )


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profiles/profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        return get_object_or_404(
            queryset, user__username=self.kwargs.get("username")
        )


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = "profiles/edit.html"
    model = Profile
    form_class = ProfileModelForm

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        return get_object_or_404(
            queryset, user__username=self.kwargs.get("username")
        )

    def get_success_url(self):
        profile_object = self.get_object()
        url = reverse(
            "profiles:profile",
            kwargs={"username": profile_object.user.username},
        )
        return url

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        profile_object = self.get_object()
        if not context.get("phone_number_formset"):
            context["phone_number_formset"] = ProfilePhoneNumberInlineFormSet(
                instance=profile_object
            )

        if not context.get("email_formset"):
            context["email_formset"] = ProfileEmailInlineFormSet(
                instance=profile_object
            )

        if not context.get("address_formset"):
            context["address_formset"] = ProfileAddressInlineFormSet(
                instance=profile_object
            )

        if not context.get("profile_form"):
            context["profile_form"] = ProfileModelForm(instance=profile_object)
        return context

    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        phone_number_formset = ProfilePhoneNumberInlineFormSet(
            request.POST,
            instance=profile,
        )
        email_formset = ProfileEmailInlineFormSet(
            request.POST,
            instance=profile,
        )
        address_formset = ProfileAddressInlineFormSet(
            request.POST,
            instance=profile,
        )

        profile_form = ProfileModelForm(
            data=request.POST,
            files=request.FILES,
            instance=profile,
        )
        if (
            profile_form.is_valid()
            and phone_number_formset.is_valid()
            and email_formset.is_valid()
            and address_formset.is_valid()
        ):
            return self.form_valid(
                address_formset,
                email_formset,
                phone_number_formset,
                profile_form,
            )

        return self.form_invalid(
            email_formset=email_formset,
            phone_number_formset=phone_number_formset,
            address_formset=address_formset,
            profile_form=profile_form,
        )

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def form_valid(
        self, address_formset, email_formset, phone_number_formset, profile_form
    ):
        self.object = profile_form.save()
        email_formset.save()
        phone_number_formset.save()
        address_formset.save()

        return HttpResponseRedirect(self.get_success_url())
