import json
import requests
from os import listdir, remove
from os.path import isfile, join
from email import message_from_string
from email.utils import make_msgid
from django.conf import settings
from django.utils import timezone
from celery import shared_task
from mails.utils import (
    save_mail_from_file,
    get_email_body,
    set_email_body,
    send_email
)
from exceptions.core import (
    MailUserNotSentError,
    MailUserNotFoundError,
    InvalidMailUserIntegrationDataError,
    ReceivedMailNotFound,
)

@shared_task(name="create_mail_user")
def create_mail_user(mail_user_id: int):
    from mails.models import UserMail

    if not mail_user_id:
        raise MailUserNotSentError()
        
    user_mail = UserMail.objects.filter(pk=mail_user_id).first()
    if not user_mail:
        raise MailUserNotFoundError({ 'pk': mail_user_id })
    
    url = "%s/add/" % settings.USER_SYSTEM_URL
    headers = {
        'Authorization': 'Bearer %s' % settings.USER_SYSTEM_AUTHORIZATION
    }
    payload = {
        "user_name": user_mail.mail_user,
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise InvalidMailUserIntegrationDataError(response.text)
    
    response_data = json.loads(response.text)
    if "data" not in response_data:
        raise InvalidMailUserIntegrationDataError(response.text)
    data = response_data["data"]
    if "user_name" not in data:
        raise InvalidMailUserIntegrationDataError(response.text)
    user_name = data["user_name"]
    user_mail.mail_user = user_name
    user_mail.mail = "%s@tunelator.com.br" % user_name
    user_mail.save()
        

@shared_task(name="send_redirect_mail")
def send_redirect_mail(user_received_mail_id: int, force: bool = False):
    from mails.models import UserReceivedMail
    
    received_mail = UserReceivedMail.objects.filter(pk=user_received_mail_id).first()
    if not received_mail:
        raise ReceivedMailNotFound({ 'pk': user_received_mail_id })

    if not received_mail.mail.redirect_enabled and not force:
        return
    
    mail_to_send = received_mail.mail.user.email
    if received_mail.mail.redirect_to:
        mail_to_send = received_mail.mail.redirect_to

    mail_msg = message_from_string(received_mail.raw_mail)
    
    del mail_msg["to"]
    mail_msg["to"] = "<%s>" % mail_to_send

    if received_mail.delivered:
        del mail_msg['Message-ID']
        mail_msg['Message-ID'] = make_msgid()
    
    text_body, html_body = get_email_body(mail_msg)
    if html_body:
        header = '' +\
            '<table border="0" cellpadding="0" cellspacing="0" width="100%">' +\
                '<tr>' +\
                    '<td bgcolor="#5F30E2" style="padding: 10px; color: #FFFFFF;">' + \
                        'Esse é um e-mail reenviado pelo <a style="color: #FFFFFF;" href="https://tunelator.com.br/">tunelator.com.br</a>.' +\
                        '<br/>' +\
                        '<br/>' +\
                        '<strong>Conta de Redirecionamento:</strong> <a style="color: #FFFFFF;" href="mailto:' + str(received_mail.mail.mail) + '">' + str(received_mail.mail.mail) + '</a>' +\
                    '</td>' +\
                '</tr>' +\
            '</table>' +\
            '<br/>'
        header = header.encode('utf-8')
        html_body = header + html_body
        html_body.decode('utf-8')
    
    if text_body:
        header = 'Esse é um e-mail reenviado pelo tunelator.com.br.\r\n\r\nConta de Redirecionamento:  ' + str(received_mail.mail.mail) + '\r\n'
        header = header.encode('utf-8')
        text_body = header + text_body
        text_body.decode('utf-8')

    set_email_body(mail_msg, text_body, html_body)

    send_email(mail_to_send, mail_msg)

    received_mail.delivered = True
    received_mail.delivered_date = timezone.now()
    received_mail.save()

@shared_task(name="check_user_late_mails")
def check_user_late_mails(user_mail_id):
    from mails.models import UserMail

    user_mail = UserMail.objects.filter(pk=user_mail_id).first()
    if not user_mail:
        MailUserNotFoundError({ 'pk': user_mail_id })
    
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
        MailUserNotFoundError({ 'pk': user_mail_id })

    save_mail_from_file(user_mail, real_path)
    remove(real_path)
