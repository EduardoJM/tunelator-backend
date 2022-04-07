import json
from django.conf import settings
from celery import shared_task
import requests

@shared_task(name="create_mail_user")
def create_mail_user(mail_user_id: int):
    from mails.models import UserMail

    if not mail_user_id:
        raise Exception("No user id was sent")
        
    user_mail = UserMail.objects.filter(pk=mail_user_id).first()
    if not user_mail:
        raise Exception("Invalid user id was sent")

    url = "%s/add/" % settings.USER_SYSTEM_URL
    
    response = requests.post(url)
    if response.status_code == 200:
        response_data = json.loads(response.text)
        if "data" not in response_data:
            raise Exception("Invalid call data")
        data = response_data["data"]
        if "user_name" not in data:
            raise Exception("Invalid call data")
        user_name = data["user_name"]
        user_mail.mail_user = user_name
        user_mail.save()
    else:
        raise Exception("Error in server: " + response.text)
