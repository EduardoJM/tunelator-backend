# Generated by Django 3.2 on 2022-04-17 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0005_alter_usermail_mail_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userreceivedmail',
            name='origin_mail',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='origin mail'),
        ),
        migrations.AlterField(
            model_name='userreceivedmail',
            name='subject',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='subject'),
        ),
    ]