# Generated by Django 3.2.14 on 2022-08-04 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SocialContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='title')),
                ('link', models.URLField(max_length=255, verbose_name='link')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='description')),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='', verbose_name='image')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'Social Content',
                'verbose_name_plural': 'Social Contents',
            },
        ),
    ]
