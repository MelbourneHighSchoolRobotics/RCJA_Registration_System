# Generated by Django 2.2.10 on 2020-02-23 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0004_auto_20200224_0021'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campus',
            options={'ordering': ['school', 'name'], 'verbose_name': 'Campus', 'verbose_name_plural': 'Campuses'},
        ),
    ]