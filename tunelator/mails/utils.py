import re
import io
from django.core.files import File
from email import message_from_string
from email.header import decode_header
from django.core.files import File
from django.utils import timezone
from mails.models import UserReceivedMail, UserReceivedMailAttachment

def decode_subject(message):
    output = message['subject']
    decoded = decode_header(output)
    if len(decoded) > 0:
        decoded_bytes, encoding = decoded[0]
        if type(decoded_bytes) == str:
            output = decoded_bytes
        else:
            output = decoded_bytes.decode(encoding)
    return output

def decode_from_email(message):
    output = message['from']
    decoded = decode_header(output)
    for decoded_item in decoded:
        decoded_bytes, encoding = decoded_item
        if not encoding:
            encoding = "utf-8"
        
        if type(decoded_bytes) == str:
            decoded_string = decoded_bytes
        else:
            decoded_string = decoded_bytes.decode(encoding).strip()

        match = re.match('^<(.*?\@.*?)>$', decoded_string)
        if match:
            return match.groups()[0]
    return output

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

def get_attachments(received_email):
    attachments = []
    for payload in received_email.get_payload():
        if payload.is_multipart():
            continue
        disposition = payload['Content-Disposition']
        if 'attachment' not in disposition:
            continue
        print(disposition)
        match = re.search('filename="(.*?)"', disposition)
        if not match:
            continue
        file_name = match.groups()[0]
        file_content = payload.get_payload(decode=True)
        attachments += [(file_content, file_name)]
    return attachments

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

    received_mail = UserReceivedMail()
    received_mail.mail = user_mail

    if not user_mail.plan_enabled:
        received_mail.delivered = True
        received_mail.delivered_date = timezone.now()

    text_body, html_body = get_email_body(email)

    received_mail.origin_mail = decode_from_email(email)
    received_mail.subject = decode_subject(email)
    received_mail.text_content = text_body
    received_mail.html_content = html_body
    received_mail.raw_mail = text
    received_mail.save()

    attachments = get_attachments(email)
    for attachment in attachments:
        file_content, file_name = attachment
        attachment_model = UserReceivedMailAttachment()
        attachment_model.received_mail=received_mail,
        attachment_model.file_name=file_name,
        attachment_model.file.save(file_name, File(io.BytesIO(file_content)))
        attachment_model.save()
