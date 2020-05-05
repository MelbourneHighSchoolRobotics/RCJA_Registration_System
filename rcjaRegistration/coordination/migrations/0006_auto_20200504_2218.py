# Generated by Django 3.0.3 on 2020-05-04 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coordination', '0005_auto_20200314_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coordinator',
            name='permissions',
            field=models.CharField(choices=[('viewall', 'View all'), ('eventmanager', 'Event manager'), ('schoolmanager', 'School manager'), ('billingmanager', 'Billing manager'), ('webeditor', 'Web editor'), ('full', 'Full')], max_length=20, verbose_name='Permissions'),
        ),
    ]
