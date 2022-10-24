from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'config.settings')

app = Celery('config') # 프로젝트 이름; config가 오히려 헷갈리나?
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Seoul')
app.config_from_object(settings, namespace="CELERY") # celery app이 django settings를 이용한다. 

app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request}')