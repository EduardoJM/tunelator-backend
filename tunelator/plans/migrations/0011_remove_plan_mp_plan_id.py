# Generated by Django 3.2 on 2022-04-23 23:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0010_approval_stripe_customer_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='mp_plan_id',
        ),
    ]
