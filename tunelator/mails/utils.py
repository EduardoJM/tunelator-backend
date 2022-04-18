import re
import io
from django.core.files import File
from email import message_from_string
from email.header import decode_header
from django.core.files import File
from django.utils import timezone
from mails.models import UserReceivedMail, UserReceivedMailAttachment

def decode_subject(message):
    output = ""
    decoded = decode_header(output)
    for decoded_bytes, encoding in decoded:
        if type(decoded_bytes) == str:
            output += decoded_bytes
        else:
            output += decoded_bytes.decode(encoding)
    return output

def decode_from_email(message):
    output = ""
    decoded = decode_header(output)
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

def save_mail_from_file(user_mail, path):
    text = None
    lines = []
    with open(path) as f:
        lines = f.readlines()
        text = "\n".join(lines)
    
    if not text:
        raise Exception("can't read file: " + path)

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
