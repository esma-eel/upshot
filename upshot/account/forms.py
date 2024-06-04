import re

from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.core.validators import ValidationError

from .models import Profile, User

GRADE_CHOICES = (("assistant", "کاردانی"), ("bachelor", "کارشناسی"))


class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        label="شناسه کاربری",
        max_length=45,
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded-pill p-4 text-center text-muted",
                "placeholder": "شناسه کاربری",
            }
        ),
    )

    email = forms.EmailField(
        label="پست الکترونیک",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded-pill p-4 text-center text-muted",
                "placeholder": "پست الکترونیک",
            }
        ),
    )

    grade = forms.ChoiceField(
        choices=GRADE_CHOICES,
        label="مقطع تحصیلی",
        widget=forms.Select(
            attrs={"class": "custom-select rounded-pill text-center text-muted"}
        ),
    )

    student_number = forms.CharField(
        label="شماره دانشجویی",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded-pill p-4 text-center text-muted",
                "placeholder": "شماره دانشجویی",
            }
        ),
    )

    password1 = forms.CharField(
        label="شناسه عبور",
        max_length=64,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control rounded-pill p-4 text-center text-muted",
                "placeholder": "شناسه عبور",
            }
        ),
    )

    password2 = forms.CharField(
        label="تایید شناسه عبور",
        max_length=64,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control rounded-pill p-4 text-center text-muted",
                "placeholder": "تایید شناسه عبور",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        query_set = User.objects.filter(email=email)
        if query_set.exists():
            raise ValidationError("این پست الکترونیک قبلا استفاده شده است")

        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        query_set = User.objects.filter(username=username)
        if query_set.exists():
            raise ValidationError("این شناسه کاربری قبلا گرفته شده است")
        return username

    def clean_student_number(self):
        student_number = self.cleaned_data["student_number"]
        query_set = Profile.objects.filter(student_number=student_number)

        if not student_number.isnumeric():
            raise ValidationError("شماره دانشجویی باید فقط شامل اعداد باشد")

        if query_set.exists():
            raise ValidationError("این شماره دانشجویی قبلا استفاده شده است")
        return student_number

    def clean(self):
        cleaned_data = super().clean()
        strong_pass = re.compile(
            (
                r'^(?=.*?\d)(?=.*?[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~])'
                r"(?=.*?[A-Z])(?=.*?[a-z])"
                r'[A-Za-z\d!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]{8,}$'
            )
        )
        pass1 = cleaned_data.get("password1")
        pass2 = cleaned_data.get("password2")

        if pass1 and pass2:
            if (pass1 == pass2) and not (strong_pass.match(pass1)):
                raise ValidationError(
                    "شناسه عبور قوی نیست، شناسه عبور باید شامل حروف"
                    " بزرگ، کوچک، عدد و کاراکتر های خاص باشد"
                )

            if pass1 != pass2:
                raise ValidationError(
                    "شناسه عبور نادرست، لطفا دوباره امتحان کنید"
                )


class PasswordResetFormEmailChecker(PasswordResetForm):

    def clean_email(self):
        to_email = self.cleaned_data["email"]
        query_set = User.objects.filter(email=to_email)

        if not query_set.exists():
            raise ValidationError(
                "هیچ حساب کاربری با این پست الکترونیکی ایجاد نشده است"
            )

        return to_email


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label="پست الکترونیک",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control rounded-pill p-4 text-center text-muted"
            }
        ),
    )

    username = forms.CharField(
        label="شناسه کاربری",
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded-pill p-4 text-center text-muted"
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": (
                        "form-control rounded-pill p-4 text-center text-muted"
                    )
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": (
                        "form-control rounded-pill p-4 text-center text-muted"
                    )
                }
            ),
        }


class ProfileEditForm(forms.ModelForm):

    grade = forms.ChoiceField(
        choices=GRADE_CHOICES,
        label="مقطع تحصیلی",
        widget=forms.Select(
            attrs={"class": "custom-select rounded-pill text-center text-muted"}
        ),
    )

    student_number = forms.IntegerField(
        label="شماره دانشجویی",
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded-pill p-4 text-center text-muted",
                "maxlength": "30",
            }
        ),
    )
    photo = forms.ImageField(label="تصویر حساب کاربری", required=False)
    about = forms.CharField(
        label="درباره من",
        widget=forms.Textarea(
            attrs={
                "class": "form-control p-4 text-right text-muted",
            }
        ),
    )

    class Meta:
        model = Profile
        fields = ["grade", "student_number", "photo", "about"]
