# Generated by Django 3.0.3 on 2020-05-01 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0003_auto_20200227_0154'),
    ]

    operations = [
        migrations.AddField(
            model_name='campus',
            name='postcode',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='Postcode'),
        ),
        migrations.AddField(
            model_name='school',
            name='postcode',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='Postcode'),
        ),
    ]
