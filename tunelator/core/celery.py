import os
import environ
from urllib.parse import quote
from datetime import timedelta
from pathlib import Path
from celery import Celery
from celery.schedules import crontab
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('tunelator')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'

if env('DEBUG'):
    BASE_REDIS_URL = env('REDIS_CELERY_URL', default=None)
    app.conf.broker_url = BASE_REDIS_URL
else:
    key = quote(env('AWS_SQS_KEY'))
    access = quote(env('AWS_SQS_ACCESS'))
    region = env('AWS_SQS_REGION')
    app.conf.broker_url = 'sqs://%s:%s@' % (key, access)
    app.conf.broker_transport_options = {
        "region": region
    }

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute="*/10"), periodic_check_mails.s())
    sender.add_periodic_task(crontab(minute="*/2"), periodic_clean_stripe_checkout_ids.s())
    sender.add_periodic_task(crontab(minute="*/2"), periodic_clean_expired_forgot_password_sessions.s())

@app.task(name="periodic_check_mails")
def periodic_check_mails():
    from mails.models import UserMail
    from mails.tasks import check_user_late_mails
    
    mails = UserMail.objects.filter(plan_enabled=True).all()    
    for mail in mails:
        check_user_late_mails.delay(mail.pk)

@app.task(name="periodic_clean_stripe_checkout_ids")
def periodic_clean_stripe_checkout_ids():
    from payments.models import SubscriptionCheckout, SubscriptionManager
    
    time = timezone.now() - timedelta(hours=6)

    SubscriptionCheckout.objects.filter(
        Q(created_at__lte=time) | Q(used=True)
    ).delete()

    SubscriptionManager.objects.filter(
        Q(created_at__lte=time) | Q(used=True)
    ).delete()

@app.task(name='periodic_clean_expired_forgot_password_sessions')
def periodic_clean_expired_forgot_password_sessions():
    from authentication.models import ForgotPasswordSession

    ForgotPasswordSession.objects.filter(
        Q(valid_until__lte=timezone.now()) | Q(used=True)
    ).delete()
