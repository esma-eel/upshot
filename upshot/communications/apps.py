from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommunicationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "upshot.communications"
    verbose_name = _("Communications")

    def ready(self):
        pass
