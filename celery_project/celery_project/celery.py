import os

from celery import Celery

app = Celery("exchange")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celery_project.settings")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
