# Generated by Django 3.0.7 on 2020-10-24 03:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_auto_20200315_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='hardwarePlatform',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='teams.HardwarePlatform', verbose_name='Hardware platform'),
        ),
        migrations.AlterField(
            model_name='team',
            name='softwarePlatform',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='teams.SoftwarePlatform', verbose_name='Software platform'),
        ),
    ]