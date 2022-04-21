from django.core.management.base import BaseCommand
from mails.models import UserReceivedMail
from mails.utils import update_mail_origin_subject

class Command(BaseCommand):
    def handle(self, *args, **options):
        received_mails = UserReceivedMail.objects.all()
        for received in received_mails:
            update_mail_origin_subject(received)
