# Generated by Django 2.2.8 on 2020-02-17 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20200217_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='division',
            name='name',
            field=models.CharField(max_length=20, unique=True, verbose_name='Name'),
        ),
    ]
