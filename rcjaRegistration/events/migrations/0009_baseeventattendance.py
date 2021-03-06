# Generated by Django 3.0.3 on 2020-03-14 12:43

import common.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0003_auto_20200227_0154'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0008_auto_20200310_2220'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseEventAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('campus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='schools.Campus', verbose_name='Campus')),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.Division', verbose_name='Division')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event', verbose_name='Event')),
                ('mentorUser', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Mentor')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='schools.School', verbose_name='School')),
            ],
            options={
                'verbose_name': 'Base attendance',
            },
            bases=(common.models.SaveDeleteMixin, models.Model),
        ),
    ]
