# Generated by Django 3.0.3 on 2020-05-04 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20200315_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', help_text="Event must be published to be visible and for people to register. Can't unpublish once people have registered.", max_length=15, verbose_name='Status'),
        ),
    ]
