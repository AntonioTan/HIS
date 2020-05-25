# Generated by Django 3.0.3 on 2020-05-15 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appoint', '0004_auto_20200420_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='weekday',
            field=models.SmallIntegerField(),
        ),
    ]