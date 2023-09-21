from django import forms
from django.utils.translation import gettext_lazy as _

from .models import MentorSetting


class MentorSettingForm(forms.ModelForm):
    choices = (
        (0, 'غیرفعال'),
        (1, 'فعال'),
    )
    active = forms.TypedChoiceField(choices=choices, coerce=int, label='وضعیت راهنما',)
    
    class Meta:
        model = MentorSetting
        fields = ("field", "email", "social_media_link", "phone_number", "extra_info", "active")

        widgets = {
            'field': forms.TextInput(attrs={"class": "form-control rounded-pill p-4 text-center text-muted"}),

            'email': forms.EmailInput(attrs={"class": "form-control rounded-pill p-4 text-center text-muted"}),

            'social_media_link': forms.URLInput(attrs={"class": "form-control rounded-pill p-4 text-center text-muted"}),
            
            'phone_number': forms.TextInput(attrs={"class": "form-control rounded-pill p-4 text-center text-muted"}),

            'extra_info': forms.Textarea(attrs={"class": "form-control p-4 text-right text-muted"}),

            'active': forms.Select(attrs={"class": "custom-select rounded-pill text-center text-muted"}),
            
        }

        labels = {
            'field': _('زمینه'),
            'email': _('پست الکترونیک'),
            'social_media_link': _('لینک شبکه اجتماعی'),
            'phone_number': _('شماره تلفن(اختیاری)'),
            'extra_info': _('اطلاعات اضافی'),
        }

        help_texts = {
            'field': _('زمینه‌ای که در آن میتوانید افراد را راهنمایی کنید'),
            'email': _(''),
            'social_media_link': _('لینک شبکه اجتماعی که از طریق آن با شاگرد خود میخواهید  ارتباط برقرار کنید'),
            'phone_number': _('این مورد اختیاری میباشد'),
            'extra_info': _('اطلاعات بیشتر درباره زمینه‌ی فعالیت و اینکه چه کار هایی برای شاگردان خود میکنید و ...'),
        }
