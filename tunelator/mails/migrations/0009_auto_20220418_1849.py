# Generated by Django 3.2 on 2022-04-18 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0008_userreceivedmail_raw_file_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userreceivedmail',
            name='html_content',
        ),
        migrations.RemoveField(
            model_name='userreceivedmail',
            name='text_content',
        ),
        migrations.DeleteModel(
            name='UserReceivedMailAttachment',
        ),
    ]
