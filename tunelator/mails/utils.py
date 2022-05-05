from email import message_from_string
from email.header import decode_header
from django.utils import timezone
from mails.models import UserReceivedMail

def decode_subject(message):
    if not message["subject"]:
        return ""
    output = ""
    decoded = decode_header(message["subject"])
    for decoded_bytes, encoding in decoded:
        if type(decoded_bytes) == str:
            output += decoded_bytes
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
    html_body = ""
    if received_email.is_multipart():
        for payload in received_email.get_payload():
            # If the message comes with a signature it can be that this
            # payload itself has multiple parts, so just return the
            # first one
            if payload.is_multipart():
                text_body, html_body = get_email_body(payload)

            body = payload.get_payload()
            if payload.get_content_type() == "text/plain":
                text_body = body
            elif payload.get_content_type() == "text/html":
                html_body = body
    else:
        text_body = received_email.get_payload()
        html_body = None
    return text_body, html_body
