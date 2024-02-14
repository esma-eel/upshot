from django import forms
from .models import ProfilePhoneNumber, Profile, ProfileEmail, ProfileAddress


class ProfilePhoneNumberModelForm(forms.ModelForm):
    class Meta:
        model = ProfilePhoneNumber
        fields = ["profile", "phone_number", "is_primary"]


class ProfileEmailModelForm(forms.ModelForm):
    class Meta:
        model = ProfileEmail
        fields = ["profile", "email", "is_primary"]


class ProfileAddressModelForm(forms.ModelForm):
    class Meta:
        model = ProfileAddress
        fields = ["profile", "city", "address", "is_primary"]


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["name", "avatar"]


ProfilePhoneNumberInlineFormSet = forms.inlineformset_factory(
    parent_model=Profile,
    model=ProfilePhoneNumber,
    form=ProfilePhoneNumberModelForm,
    fields=ProfilePhoneNumberModelForm.Meta.fields,
    exclude=["profile"],
    extra=1,
    max_num=3,
    can_delete=True,
    can_delete_extra=False,
)

ProfileEmailInlineFormSet = forms.inlineformset_factory(
    parent_model=Profile,
    model=ProfileEmail,
    form=ProfileEmailModelForm,
    fields=ProfileEmailModelForm.Meta.fields,
    exclude=["profile"],
    extra=1,
    max_num=3,
    can_delete=True,
    can_delete_extra=False,
)

ProfileAddressInlineFormSet = forms.inlineformset_factory(
    parent_model=Profile,
    model=ProfileAddress,
    form=ProfileAddressModelForm,
    fields=ProfileAddressModelForm.Meta.fields,
    exclude=["profile"],
    extra=1,
    max_num=3,
    can_delete=True,
    can_delete_extra=False,
)
