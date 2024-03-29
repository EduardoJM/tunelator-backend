import smtplib
from django.conf import settings
from email import message_from_string
from email.header import decode_header
from email.charset import Charset, add_charset
from django.utils import timezone
from mails.models import UserReceivedMail
from exceptions.core import FileReadError

def decode_subject(message):
    if not message["subject"]:
        return ""
    output = ""
    decoded = decode_header(message["subject"])
    for decoded_bytes, encoding in decoded:
        if not decoded_bytes:
            pass
        if type(decoded_bytes) == str:
            output += decoded_bytes
        else:
            if not encoding:
                output += decoded_bytes.decode()
            else:
                output += decoded_bytes.decode(encoding)
    return output

def decode_from_email(message):
    if not message["from"]:
        return ""
    output = ""
    decoded = decode_header(message["from"])
    for decoded_item in decoded:
        decoded_bytes, encoding = decoded_item
        if not encoding:
            encoding = "utf-8"
        
        if type(decoded_bytes) == str:
            decoded_string = decoded_bytes
        else:
            decoded_string = decoded_bytes.decode(encoding).strip()

        output += decoded_string
    return output

def update_mail_origin_subject(received_mail):
    text = received_mail.raw_mail
    email = message_from_string(text)

    received_mail.origin_mail = decode_from_email(email)
    received_mail.subject = decode_subject(email)
    received_mail.save()

def save_mail_from_file(user_mail, path):
    text = None
    lines = []
    with open(path) as f:
        lines = f.readlines()
        text = "\n".join(lines)
    
    if not text:
        raise FileReadError(path)

    text = "".join([s for s in text.strip().splitlines(True) if s.strip("\r\n").strip()])
    email = message_from_string(text)

    received_mail = UserReceivedMail.objects.filter(raw_file_path=path).first()
    if not received_mail:
        received_mail = UserReceivedMail()

    received_mail.mail = user_mail

    if not user_mail.plan_enabled:
        received_mail.delivered = True
        received_mail.delivered_date = timezone.now()

    received_mail.origin_mail = decode_from_email(email)
    received_mail.subject = decode_subject(email)
    received_mail.raw_mail = text
    received_mail.raw_file_path = path
    received_mail.save()


def set_email_body(received_email, text_body, html_body):
    if not received_email.is_multipart():
        if not text_body:
            return
        received_email.set_payload(text_body, charset='utf-8')
        return

    for payload in received_email.get_payload():
        if payload.is_multipart():
            set_email_body(payload, text_body, html_body)
            continue
        
        if text_body:
            if payload.get_content_type() == "text/plain":
                payload.set_payload(text_body, charset='utf-8')
        
        if html_body:
            if payload.get_content_type() == "text/html":
                payload.set_payload(html_body, charset='utf-8')


def get_email_body(received_email):
    text_body = ""
    text_encoding = None
    html_body = ""
    html_encoding = None
    if received_email.is_multipart():
        for payload in received_email.get_payload():
            # If the message comes with a signature it can be that this
            # payload itself has multiple parts, so just return the
            # first one
            if payload.is_multipart():
                text_body, text_encoding, html_body, html_encoding = get_email_body(payload)
            else:
                body = payload.get_payload(decode=True)
                encoding = payload.get_content_charset()
                if payload.get_content_type() == "text/plain":
                    text_body = body
                    text_encoding = encoding
                elif payload.get_content_type() == "text/html":
                    html_body = body
                    html_encoding = encoding
    else:
        text_body = received_email.get_payload(decode=True)
        text_encoding = received_email.get_content_charset()
        html_body = None
    return text_body, text_encoding, html_body, html_encoding

def send_email(mail_to_send: str, mail_msg: str):
    with smtplib.SMTP(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT) as s:
        print(s)
        print(s.sendmail)
        s.ehlo()
        s.starttls()
        s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        s.sendmail(
            settings.EMAIL_HOST_USER,
            mail_to_send,
            mail_msg.as_string()
        )
        s.quit()
