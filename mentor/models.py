from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class MentorSetting(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    field = models.CharField(max_length=255)
    email = models.EmailField()
    social_media_link = models.URLField()
    phone_number = models.CharField(max_length=36, blank=True, null=True)
    extra_info = models.TextField()

    active = models.BooleanField(default=False)

    def __str__(self):
        return "تنظیمات راهنمایی کاربر {}".format(self.user)


class MentorRequest(models.Model):
    user_from = models.ForeignKey(
        "auth.User", related_name="ment_from_set", on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        "auth.User", related_name="ment_to_set", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    approved = models.BooleanField(default=False)
    objects = models.Manager()  # save

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return "درخواست راهنمایی از طرف {fm} به {to}".format(
            fm=self.user_from, to=self.user_to
        )


# add a field named mentors which is foreign key to User and
# show query of users who are requested to be users mentor
User.add_to_class(
    "mentors",
    models.ManyToManyField(
        "self", through=MentorRequest, related_name="mentor", symmetrical=False
    ),
)
