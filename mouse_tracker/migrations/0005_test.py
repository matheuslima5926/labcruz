# Generated by Django 2.2.4 on 2019-08-21 00:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mouse_tracker', '0004_delete_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_start', models.DateTimeField(auto_now=True)),
                ('datetime_end', models.DateTimeField(null=True)),
                ('entrances_close_right', models.IntegerField(default=0)),
                ('entrances_close_left', models.IntegerField(default=0)),
                ('entrances_open_right', models.IntegerField(default=0)),
                ('entrances_open_left', models.IntegerField(default=0)),
                ('timein_close_right', models.FloatField(default=0.0)),
                ('timein_close_left', models.FloatField(default=0.0)),
                ('timein_open_right', models.FloatField(default=0.0)),
                ('timein_open_left', models.FloatField(default=0.0)),
                ('time_moving', models.FloatField(default=0.0)),
                ('time_idle', models.FloatField(default=0.0)),
                ('max_speed', models.FloatField(default=0.0)),
                ('min_speed', models.FloatField(default=0.0)),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mouse_tracker.Animal')),
                ('maze', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mouse_tracker.Maze')),
            ],
        ),
    ]
