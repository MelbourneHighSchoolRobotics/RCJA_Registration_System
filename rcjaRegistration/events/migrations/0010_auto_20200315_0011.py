# Generated by Django 3.0.3 on 2020-03-14 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_baseeventattendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='eventType',
            field=models.CharField(choices=[('competition', 'Competition'), ('workshop', 'Workshop')], help_text='Competition is standard event with teams and students. Workshop has no teams or students, just workshop attendees.', max_length=15, verbose_name='Event type'),
        ),
    ]
