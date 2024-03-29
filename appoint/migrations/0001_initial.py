# Generated by Django 3.0.3 on 2020-04-19 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0003_auto_20200418_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=30)),
                ('type', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('sex', models.BooleanField()),
                ('title', models.CharField(max_length=30)),
                ('strength', models.CharField(max_length=50)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appoint.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('morning_registration_num', models.SmallIntegerField()),
                ('afternoon_registration_num', models.SmallIntegerField()),
                ('weekday', models.SmallIntegerField(max_length=1)),
                ('type', models.BooleanField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appoint.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.BooleanField()),
                ('start_time', models.DateTimeField()),
                ('price', models.SmallIntegerField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appoint.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_time', models.DateTimeField(null=True)),
                ('valid', models.BooleanField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.User')),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appoint.Registration')),
            ],
        ),
    ]
