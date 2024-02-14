from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdminstrationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "upshot.adminstration"
    verbose_name = _("Adminstration")

    def ready(self):
        pass
