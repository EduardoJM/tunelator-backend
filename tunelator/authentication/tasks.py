from celery import shared_task
from django.contrib.auth import get_user_model
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from authentication.exceptions import UserNotFoundError

User = get_user_model()

@shared_task(name="send_recovery_link")
def send_recovery_link(email: str):
    from authentication.models import ForgotPasswordSession

    user = User.objects.filter(email=email).first()
    if not user:
        raise UserNotFoundError({ 'email': email })
    
    session = ForgotPasswordSession()
    session.user = user
    session.save()

    html = render_to_string('password-reset.html', {
        'session': session
    })

    mail.send_mail(
        'Recuperar sua senha',
        message='',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
        html_message=html,
    )
