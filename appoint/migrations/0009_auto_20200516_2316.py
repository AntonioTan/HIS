# Generated by Django 3.0.3 on 2020-05-16 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appoint', '0008_auto_20200516_2305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='afternoon_registration_num',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='morning_registration_num',
        ),
        migrations.AddField(
            model_name='schedule',
            name='morning_afternoon',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='schedule',
            name='num',
            field=models.SmallIntegerField(default=0),
        ),
    ]
