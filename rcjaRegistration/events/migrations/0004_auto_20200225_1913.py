# Generated by Django 2.2.10 on 2020-02-25 08:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20200225_1547'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='maxMembersPerTeam',
            new_name='event_maxMembersPerTeam',
        ),
        migrations.RemoveField(
            model_name='event',
            name='availableDivisions',
        ),
        migrations.RemoveField(
            model_name='event',
            name='entryFee',
        ),
        migrations.AddField(
            model_name='event',
            name='eventType',
            field=models.CharField(choices=[('competition', 'Competition'), ('workshop', 'Workshop')], default='competition', help_text='Competition is standard event with teams and students. Workshop has no teams or students, just workshop attendees.', max_length=15, verbose_name='Event type'),
        ),
        migrations.AddField(
            model_name='event',
            name='event_billingType',
            field=models.CharField(choices=[('team', 'By team'), ('student', 'By student')], default='team', max_length=15, verbose_name='Billing type'),
        ),
        migrations.AddField(
            model_name='event',
            name='event_defaultEntryFee',
            field=models.PositiveIntegerField(default=1, verbose_name='Default entry fee'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='event_maxTeamsForEvent',
            field=models.PositiveIntegerField(blank=True, help_text='Leave blank for no limit. Only enforced in the mentor signup page, can be overridden in the admin portal.', null=True, verbose_name='Max teams for event'),
        ),
        migrations.AddField(
            model_name='event',
            name='event_maxTeamsPerSchool',
            field=models.PositiveIntegerField(blank=True, help_text='Leave blank for no limit. Only enforced in the mentor signup page, can be overridden in the admin portal.', null=True, verbose_name='Max teams per school'),
        ),
        migrations.AddField(
            model_name='event',
            name='event_specialRateFee',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Special rate fee'),
        ),
        migrations.AddField(
            model_name='event',
            name='event_specialRateNumber',
            field=models.PositiveIntegerField(blank=True, help_text='The number of teams/ students specified will be billed at this rate. Subsequent teams/ students will be billed at the default rate. Leave blank for no special rate.', null=True, verbose_name='Special rate number'),
        ),
        migrations.AlterField(
            model_name='event',
            name='directEnquiriesTo',
            field=models.ForeignKey(help_text="This person's name and email will appear on the event page", on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Direct enquiries to'),
        ),
    ]
