from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProfilesConfig(AppConfig):
    name = "upshot.profiles"
    verbose_name = _("Profiles")

    def ready(self):
        pass
        # import upshot.profiles.signals
