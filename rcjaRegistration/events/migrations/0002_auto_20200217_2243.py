# Generated by Django 2.2.8 on 2020-02-17 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='division',
            options={'ordering': ['name'], 'verbose_name': 'Division'},
        ),
        migrations.RemoveField(
            model_name='division',
            name='state',
        ),
    ]