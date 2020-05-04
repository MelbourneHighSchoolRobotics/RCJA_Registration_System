# Generated by Django 3.0.3 on 2020-05-04 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0004_remove_state_treasurer'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='typeRegistration',
            field=models.BooleanField(default=False, help_text='Use this state in the registration portal. Once enabled cannot be disabled.', verbose_name='Registration'),
        ),
        migrations.AddField(
            model_name='state',
            name='typeWebsite',
            field=models.BooleanField(default=False, help_text='Display this state on the public website.', verbose_name='Website'),
        ),
    ]
