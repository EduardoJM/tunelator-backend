import os
import re
import inotify.adapters
from django.core.management.base import BaseCommand
from django.utils import timezone
from mails.models import UserMail, UserReceivedMail

def get_mail_informations(path):
    text = None
    lines = []
    with open(path) as f:
        lines = f.readlines()
        text = "\n".join(lines)
    if not text:
        raise Exception("can not read file: " + path)
    
    origin_match = re.search("^From:.*?<(.*?)>$", text)
    origin_mail = ""
    if origin_match:
        origin_mail = origin_match.groups()[0]
    
    subject_match = re.search("^Subject: (.*?)$", text)
    subject = ""
    if subject_match:
        subject = subject_match.groups()[0]
    
    text_content_lines = []
    capturing = False
    for line in lines:
        if line.startswith("Content-Type: text/plain;"):
            capturing = True
        elif capturing and line.startswith("--"):
            capturing = False

        if capturing:
            text_content_lines += [line]

    text_content = "\n".join(text_content_lines)

    html_content_lines = []
    capturing = False
    for line in lines:
        if line.startswith("Content-Type: text/html;"):
            capturing = True
        elif capturing and line.startswith("--"):
            capturing = False

        if capturing:
            html_content_lines += [line]

    html_content = "\n".join(html_content_lines)

    return (
        origin_mail,
        subject,
        text_content,
        html_content,
        text
    )

class Command(BaseCommand):
    def handle(self, *args, **options):
        i = inotify.adapters.InotifyTree('/home/')
        for event in i.event_gen():
            try:
                if not event:
                    continue
                (_, type_names, path, filename) = event

                if 'IN_MOVED_TO' not in type_names:
                    continue
                if not str(path).endswith('/Mail/Inbox/new'):
                    continue

                real_path = os.path.join(path, filename)
                print("MAIL REVEIVED WITH REAL PATH: {}".format(real_path))
                user_name = str(path).replace("/home/", "").replace("/Mail/Inbox/new", "").strip().lower()

                user_mail = UserMail.objects.filter(
                    mail_user__iexact=user_name
                ).first()
                
                if not user_mail:
                    print("No user associated, skipping for now.")
                    continue

                received_mail = UserReceivedMail()
                received_mail.mail = user_mail

                if not user_mail.plan_enabled:
                    received_mail.delivered = True
                    received_mail.delivered_date = timezone.now()

                origin_mail, subject, text_content, html_content, raw = get_mail_informations(real_path)

                received_mail.origin_mail = origin_mail
                received_mail.subject = subject
                received_mail.text_content = text_content
                received_mail.html_content = html_content
                received_mail.raw_mail = raw
                received_mail.save()

                os.remove(real_path)
            except Exception as e:
                print(e)
                pass
