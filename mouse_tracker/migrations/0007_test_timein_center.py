# Generated by Django 2.2.4 on 2019-10-19 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mouse_tracker', '0006_auto_20191019_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='timein_center',
            field=models.FloatField(default=0.0),
        ),
    ]