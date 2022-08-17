import os
from celery import Celery
from report_exchange.Base.base import Base

os.environ.setdefault(Base.DJANGO_SETTINGS_MODULE, Base.celery_project_settings)
app = Celery(Base.report_exchange)
app.config_from_object(Base.django_conf_settings, namespace=Base.CELERY)
