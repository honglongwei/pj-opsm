from __future__ import absolute_import

import os
import django

from celery import Celery, platforms
from django.conf import settings

platforms.C_FORCE_ROOT = True
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pj_opsm.settings')
#django.setup()

app = Celery('pj_opsm')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
