import json
import smtplib
from os import listdir, remove
from os.path import isfile, join
from email import message_from_string
from django.conf import settings
from django.utils import timezone
from celery import shared_task
from mails.notification_types import MAIL_IS_DONE
from mails.utils import save_mail_from_file
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
    headers = {
        'Authorization': 'Bearer %s' % settings.USER_SYSTEM_AUTHORIZATION
    }
    payload = {
        "user_name": user_mail.mail_user,
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        response_data = json.loads(response.text)
        if "data" not in response_data:
            raise Exception("Invalid call data")
        data = response_data["data"]
        if "user_name" not in data:
            raise Exception("Invalid call data")
        user_name = data["user_name"]
        user_mail.mail_user = user_name
        user_mail.mail = "%s@tunelator.com.br" % user_name
        user_mail.save()
    else:
        raise Exception("Error in server: " + response.text)

@shared_task(name="send_redirect_mail")
def send_redirect_mail(user_received_mail_id: int):
    from mails.models import UserReceivedMail
    
    received_mail = UserReceivedMail.objects.filter(pk=user_received_mail_id).first()
    if not received_mail:
        raise Exception("No received mail found with id " + user_received_mail_id)
    
    mail_to_send = received_mail.mail.user.email
    mail_msg = message_from_string(received_mail.raw_mail)
    
    del mail_msg["to"]
    mail_msg["to"] = "<%s>" % mail_to_send

    with smtplib.SMTP(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT) as s:
        s.ehlo()
        s.starttls()
        s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        s.sendmail(
            settings.EMAIL_HOST_USER,
            mail_to_send,
            mail_msg.as_string()
        )
        s.quit()

    if not received_mail.delivered:
        received_mail.delivered = True
        received_mail.delivered_date = timezone.now()
        received_mail.save()

@shared_task(name="check_user_late_mails")
def check_user_late_mails(user_mail_id):
    from mails.models import UserMail

    user_mail = UserMail.objects.filter(pk=user_mail_id).first()
    if not user_mail:
        raise Exception("User mail not found")
    
    path_to_find = "/home/%s/Mail/Inbox/new" % user_mail.mail_user
    
    onlyfiles = [f for f in listdir(path_to_find) if isfile(join(path_to_find, f))]

    for file in onlyfiles:
        real_path = join(path_to_find, file)
        save_user_late_mail.delay(user_mail_id, real_path)

@shared_task(name="save_user_late_mail")
def save_user_late_mail(user_mail_id, real_path):
    from mails.models import UserMail

    user_mail = UserMail.objects.filter(pk=user_mail_id).first()
    if not user_mail:
        raise Exception("User mail not found")

    save_mail_from_file(user_mail, real_path)
    remove(real_path)
