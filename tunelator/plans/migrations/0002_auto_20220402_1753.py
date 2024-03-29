# Generated by Django 3.2 on 2022-04-02 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='plandisplayfeature',
            options={'ordering': ['order'], 'verbose_name': 'plan display feature', 'verbose_name_plural': 'plan display features'},
        ),
        migrations.AddField(
            model_name='plandisplayfeature',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False, verbose_name='order'),
        ),
    ]
