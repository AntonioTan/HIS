# Generated by Django 3.0.3 on 2020-05-16 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appoint', '0005_auto_20200515_0627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='valid',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='schedule',
            name='price',
            field=models.SmallIntegerField(default=80),
        ),
        migrations.AlterField(
            model_name='order',
            name='registration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appoint.Schedule'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appoint.Doctor'),
        ),
        migrations.DeleteModel(
            name='Registration',
        ),
    ]
