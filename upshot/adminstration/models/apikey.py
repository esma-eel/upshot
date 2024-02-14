from django.db import models
from upshot.common.mixins import ModelMixin


class APIKey(ModelMixin):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=16, unique=True)
    description = models.TextField(null=True, blank=True)

    key = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.code})"
