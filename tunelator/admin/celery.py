import os
import environ
from pathlib import Path
from celery import Celery

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

BASE_REDIS_URL = env('REDIS_CELERY_URL', default=None)

if not BASE_REDIS_URL:
    exit(1)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')

app = Celery('tunelator')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.broker_url = BASE_REDIS_URL

app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'
