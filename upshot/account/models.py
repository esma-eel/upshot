from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    following = models.ManyToManyField(
        "self",
        through="account.Contact",
        related_name="followers",
        symmetrical=False,
    )

    mentors = (
        models.ManyToManyField(
            "self",
            through="mentor.MentorRequest",
            related_name="mentor",
            symmetrical=False,
        ),
    )


class Profile(models.Model):
    GRADE_CHOICES = (("assistant", "کاردانی"), ("bachelor", "کارشناسی"))
    user = models.OneToOneField("account.User", on_delete=models.CASCADE)
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    student_number = models.CharField(max_length=30)
    photo = models.ImageField(upload_to="users/%Y/%m/%d", blank=True)
    about = models.TextField(blank=True, default="")
    objects = models.Manager

    def __str__(self):
        return "پروفایل کاربر {}".format(self.user.username)


class Contact(models.Model):
    user_from = models.ForeignKey(
        "account.User", related_name="rel_from_set", on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        "account.User", related_name="rel_to_set", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return "{fm} دنبال میکند {to}".format(
            fm=self.user_from, to=self.user_to
        )
