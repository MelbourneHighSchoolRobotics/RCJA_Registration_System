# Generated by Django 3.0.3 on 2020-05-04 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0004_auto_20200505_1353'),
        ('events', '0012_event_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseeventattendance',
            name='event',
            field=models.ForeignKey(limit_choices_to={'status': 'published'}, on_delete=django.db.models.deletion.CASCADE, to='events.Event', verbose_name='Event'),
        ),
        migrations.AlterField(
            model_name='division',
            name='state',
            field=models.ForeignKey(blank=True, help_text='Leave blank for a global division. Global divisions are only editable by global administrators.', limit_choices_to={'typeRegistration': True}, null=True, on_delete=django.db.models.deletion.PROTECT, to='regions.State', verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='event',
            name='state',
            field=models.ForeignKey(limit_choices_to={'typeRegistration': True}, on_delete=django.db.models.deletion.PROTECT, to='regions.State', verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='state',
            field=models.ForeignKey(limit_choices_to={'typeRegistration': True}, on_delete=django.db.models.deletion.PROTECT, to='regions.State', verbose_name='State'),
        ),
    ]
