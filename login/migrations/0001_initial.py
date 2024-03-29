# Generated by Django 3.0.3 on 2020-04-12 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('birth', models.DateField()),
                ('age', models.SmallIntegerField()),
                ('phone', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('sign_up_time', models.DateTimeField()),
                ('appoint_times', models.SmallIntegerField()),
                ('appoint_available', models.BooleanField()),
            ],
        ),
    ]
