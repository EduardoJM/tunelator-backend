# Generated by Django 3.2 on 2022-04-17 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0007_auto_20220417_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='userreceivedmail',
            name='raw_file_path',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='raw file path'),
        ),
    ]
