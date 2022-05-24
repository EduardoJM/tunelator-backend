from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task(name="send_recovery_link")
def send_recovery_link(email: str):
    from authentication.models import ForgotPasswordSession

    user = User.objects.filter(email=email).first()
    if not user:
        raise Exception('user-not-found')
    
    session = ForgotPasswordSession()
    session.user = user
    session.save()

    # TODO: send e-mail here
