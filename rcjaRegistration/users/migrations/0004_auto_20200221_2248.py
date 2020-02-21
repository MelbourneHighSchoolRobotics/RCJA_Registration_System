# Generated by Django 2.2.8 on 2020-02-21 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200221_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='homeRegion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='regions.Region', verbose_name='Home region'),
        ),
        migrations.AlterField(
            model_name='user',
            name='homeState',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='regions.State', verbose_name='Home state'),
        ),
    ]
