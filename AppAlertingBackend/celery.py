from __future__ import absolute_import, unicode_literals
import os
import logging
import threading

import wsgiserver

from django.conf import settings
from celery import Celery
from celery.schedules import crontab
from prometheus_client import multiprocess
from prometheus_client import generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST, Gauge, Counter

from . import project_env


logger = logging.getLogger("tasks")


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# APP_NAME = BASE_DIR.rsplit("/", 1)[-1]

# ENV_CHOICES = ("DEV", "FAT", "PRO")
# ENV = os.environ.get("ENV")
# settings = "settings_pro" if ENV == "PRO" else "settings"
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{APP_NAME}.{settings}')
# os.environ["DJANGO_SETTINGS_MODULE"] = settings


# project_env.set_django_settings_env()
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AppAlertingBackend.settings')
settings_name = project_env.get_django_settings()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_name)

app = Celery(project_env.APP_NAME)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'sync_history': {
        'task': 'withdraw.tasks.sync_history',
        'schedule': 3
    },
    'sync_account_balance': {
        'task': 'withdraw.tasks.sync_account_balance',
        'schedule': crontab()
    },
    'settlement_account_daily': {
        'task': 'withdraw.tasks.settlement_account_daily',
        'schedule': crontab(minute=0, hour=0)
    },
}
app.conf.enable_utc = False
app.conf.timezone = "Asia/Shanghai"


def metrics(environ, start_response):
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    # return Response(data, mimetype=CONTENT_TYPE_LATEST)

    status = '200 OK'
    response_headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, response_headers)
    return [data]


def start_server():
    server = wsgiserver.WSGIServer(metrics, host="0.0.0.0", port=settings.CELERY_PROMETHEUS_PORT)
    server.start()


class PrometheusServer(threading.Thread):

    def metrics(self, environ, start_response):
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
        data = generate_latest(registry)
        # return Response(data, mimetype=CONTENT_TYPE_LATEST)

        status = '200 OK'
        response_headers = [('Content-type', CONTENT_TYPE_LATEST), ('Content-Length', str(len(data)))]
        start_response(status, response_headers)
        return [data]

    def run(self) -> None:
        server = wsgiserver.WSGIServer(self.metrics, host="0.0.0.0", port=settings.CELERY_PROMETHEUS_PORT)
        server.start()


IS_CELERY = os.getenv("IS_CELERY")
print(f"IS_CELERY: {IS_CELERY}")
logger.info(f"IS_CELERY: {IS_CELERY}")

if os.getenv("IS_CELERY"):
    prometheus_server = PrometheusServer()
    prometheus_server.start()
    print("prometheus_server start completed")


# @celery.task(celery.Strategy=shutdown_after_strategy)
# def shutdown_after():
#     print('will shutdown after this')