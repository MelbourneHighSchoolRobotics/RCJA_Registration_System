# Generated by Django 2.2.10 on 2020-02-26 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('permissions', models.CharField(choices=[('viewall', 'View all'), ('eventmanager', 'Event manager'), ('schoolmanager', 'School manager'), ('billingmanager', 'Billing manager'), ('full', 'Full')], max_length=20, verbose_name='Permissions')),
                ('position', models.CharField(max_length=50, verbose_name='Position')),
            ],
            options={
                'verbose_name': 'Coordinator',
                'ordering': ['state', 'user'],
            },
        ),
    ]
