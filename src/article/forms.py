from django import forms
from django.utils.translation import gettext_lazy as _
from taggit.forms import TagWidget

from .models import Article, Comment

CHOICES_SEARCH = [
    ("search_article", "مقاله"),
    ("search_author", "نویسنده"),
    ("search_tag", "برچسب"),
    ("search_guide", "راهنما"),
]


class SearchForm(forms.Form):
    """
    Search 'query' field between the type selected in 'search' field
    """

    query = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded-pill p-4 mx-1  text-muted",
                "placeholder": "جستجو‌ی مقاله، نویسنده، ...",
            }
        ),
    )

    search = forms.ChoiceField(
        choices=CHOICES_SEARCH,
        required=True,
        widget=forms.Select(
            attrs={
                "class": (
                    "custom-select mx-1 px-md-5 rounded-pill"
                    " text-center text-muted"
                ),
                "style": "height:51px;",
            }
        ),
    )


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(
                attrs={"class": "form-control p-4 text-right text-muted"}
            ),
        }

        labels = {"body": _("")}


class ArticleCreateEditForm(forms.ModelForm):
    picture = forms.ImageField(label="تصویر مقاله", required=False)

    class Meta:
        model = Article
        fields = ["title", "tags", "picture", "body", "publish", "status"]

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control rounded-pill p-4  text-muted"}
            ),
            "tags": TagWidget(
                attrs={
                    "class": "mb-3 form-control rounded-pill p-4  text-muted"
                }
            ),
            "publish": forms.DateTimeInput(
                attrs={"class": "form-control rounded-pill p-4  text-muted"}
            ),
            "status": forms.Select(
                attrs={"class": "custom-select rounded-pill  text-muted"}
            ),
        }

        labels = {
            "title": _("عنوان"),
            "tags": _("برچسب ها"),
            "slug": _("آدرس"),
            "picture": _("تصویر مقاله"),
            "publish": _("زمان انتشار"),
            "status": _("وضعیت"),
            "body": _(""),
        }

        help_texts = {
            "tags": _('تمام کلمات را با فاصله یا علامت "," جدا کنید'),
        }
