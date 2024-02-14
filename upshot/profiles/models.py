from django.conf import settings
from django.db import models
from upshot.common.mixins import ModelMixin
from .utils.upload_path import profile_upload


class Profile(ModelMixin):
    GRADE_CHOICES = (("assistant", "کاردانی"), ("bachelor", "کارشناسی"))
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    student_number = models.CharField(max_length=30)
    photo = models.ImageField(upload_to=profile_upload, blank=True)
    about = models.TextField(blank=True, default="")
    objects = models.Manager

    def __str__(self):
        return "پروفایل کاربر {}".format(self.user.username)
