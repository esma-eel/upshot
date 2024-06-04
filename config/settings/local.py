"""
This is the settings file that you use when
you’re working on the project locally. Lo-
cal development-specific settings include
DEBUG mode, log level, and activation of
developer tools like django-debug-toolbar.
"""
from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_BACKEND = get_env_variable("EMAIL_BACKEND")  # noqa
EMAIL_HOST = get_env_variable("EMAIL_HOST")  # noqa
EMAIL_PORT = get_env_variable("EMAIL_PORT")  # noqa
# EMAIL_USE_TLS = get_env_variable()  # noqa
EMAIL_HOST_USER = get_env_variable("EMAIL_HOST_USER")  # noqa
EMAIL_HOST_PASSWORD = get_env_variable("EMAIL_HOST_PASSWORD")  # noqa
PROJECT_EMAIL = get_env_variable("PROJECT_EMAIL")  # noqa

INSTALLED_APPS += []  # noqa

TEST_RUNNER = "redgreenunittest.django.runner.RedGreenDiscoverRunner"
print("local")
