# Generated by Django 2.2.10 on 2020-03-07 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0002_state_treasurer'),
        ('events', '0005_auto_20200305_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='division',
            name='state',
            field=models.ForeignKey(blank=True, help_text='Leave blank for a global division. Global divisions are only editable by global administrators.', null=True, on_delete=django.db.models.deletion.PROTECT, to='regions.State', verbose_name='State'),
        ),
    ]
