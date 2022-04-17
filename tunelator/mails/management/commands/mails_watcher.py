import os
import inotify.adapters
from django.core.management.base import BaseCommand
from mails.models import UserMail
from mails.utils import save_mail_from_file

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("begin mails watcher")
        i = inotify.adapters.InotifyTree('/home/')
        for event in i.event_gen():
            if not event:
                continue
            (_, type_names, path, filename) = event
            print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(path, filename, type_names))
            try:
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

                save_mail_from_file(user_mail, real_path)

                os.remove(real_path)
            except Exception as e:
                print(e)
                pass
