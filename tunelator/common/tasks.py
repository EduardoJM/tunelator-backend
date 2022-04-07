from django.utils.translation import gettext_lazy as _
from celery import shared_task
from firebase_admin import messaging

@shared_task(name=_('send silent notification'))
def send_silent_notification(user_id, data):
    from authentication.models import User, UserFCMToken

    user = User.objects.filter(pk=user_id).first()
    if not user:
        raise Exception("invalid user id")
    
    tokens = UserFCMToken.objects.filter(user=user).all()
    if len(tokens) == 0:
        raise Exception("no tokens registered for user")

    for token in tokens:
        try:
            message = messaging.Message(
                data=data,
                token=str(token),
            )
            messaging.send(message)
        except:
            token.delete()
