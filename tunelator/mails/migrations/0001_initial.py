# Generated by Django 3.2 on 2022-04-07 01:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('mail_user', models.CharField(default=None, max_length=32, null=True, verbose_name='mail user')),
                ('mail', models.CharField(default=None, max_length=255, null=True, verbose_name='mail')),
                ('redirect_enabled', models.BooleanField(default=True, verbose_name='redirect enabled')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mails', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'user mail',
                'verbose_name_plural': 'user mails',
            },
        ),
    ]
