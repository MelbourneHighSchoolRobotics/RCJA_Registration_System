# Generated by Django 2.2.10 on 2020-02-28 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20200228_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='entryFeeIncludesGST',
            field=models.BooleanField(default=True, help_text='Whether the prices specified on this page are GST inclusive or exclusive.', verbose_name='Includes GST'),
        ),
        migrations.AddField(
            model_name='event',
            name='globalEvent',
            field=models.BooleanField(default=False, help_text='Global events appear to users as not belonging to a state. Recommeneded for national events. Billing still uses state based settings.', verbose_name='Global event'),
        ),
    ]
