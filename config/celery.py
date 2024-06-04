import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")


celery_app = Celery("config")
task_files = [
]


celery_app.config_from_object("django.conf:settings", namespace="CELERY")

celery_app.autodiscover_tasks(task_files)


@celery_app.task  # (bind=True)
def prove_of_working():
    return "If you are reading this, celery is working."


celery_app.conf.beat_schedule = {}
