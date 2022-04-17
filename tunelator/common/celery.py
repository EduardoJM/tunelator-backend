import os
import environ
from pathlib import Path
from celery import Celery
from celery.schedules import crontab

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
BASE_REDIS_URL = env('REDIS_CELERY_URL', default=None)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('tunelator')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.broker_url = BASE_REDIS_URL
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute="*/10"), periodic_check_mails.s())

@app.task(name="periodic_check_mails")
def periodic_check_mails():
    from mails.models import UserMail
    from mails.tasks import check_user_late_mails
    
    mails = UserMail.objects.filter(plan_enabled=True).all()    
    for mail in mails:
        check_user_late_mails.delay(mail.pk)
