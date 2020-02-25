# Generated by Django 2.2.10 on 2020-02-24 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0005_auto_20200224_0127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schooladministrator',
            name='campus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='schools.Campus', verbose_name='Campus'),
        ),
    ]