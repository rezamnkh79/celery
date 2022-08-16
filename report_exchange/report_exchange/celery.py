import os
from celery import Celery
from report_exchange.Base.base import Base

os.environ.setdefault(Base.DJANGO_SETTINGS_MODULE, Base.celery_project_settings)
app = Celery(Base.report_exchange)
app.config_from_object(Base.django_conf_settings, namespace=Base.CELERY)

# app.autodiscover_tasks()
#
# app.conf.beat_schedule = {
#     'get_coins_data_30s': {
#         'task': 'account.tasks.schedule_send_email',
#         'schedule': 10.0
#     }
# }

# from celery import Celery
from celery.schedules import crontab
#
# app = Celery()

#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#
#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(3.0, test.s('world'), expires=10)
#
#     # Executes every Monday morning at 7:30 a.m.
#     # sender.add_periodic_task(
#     #     crontab(hour=7, minute=30, day_of_week=1),
#     #     test.s('Happy Mondays!'),
#     # )
#
#
# @app.task
# def test(arg):
#     print(arg)
#
#
# @app.task
# def add(x, y):
#     z = x + y
#     print(z)
