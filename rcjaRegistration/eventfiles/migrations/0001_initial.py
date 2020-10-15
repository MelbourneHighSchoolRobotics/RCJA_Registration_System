# Generated by Django 3.0.7 on 2020-10-14 04:16

import common.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import rcjaRegistration.storageBackends


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0014_auto_20201014_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentorEventFileType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='Name')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='Description')),
                ('maxFilesizeMB', models.PositiveIntegerField(default=100, verbose_name='Max file size (MB)')),
                ('allowedFileTypes', models.CharField(blank=True, help_text='Comma separated list allowed file types, leave blank for no restrictions', max_length=200, verbose_name='Allowed file types')),
            ],
            options={
                'verbose_name': 'Mentor Event File Type',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MentorEventFileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('comments', models.TextField(blank=True, verbose_name='Comments')),
                ('fileUpload', common.fields.UUIDFileField(original_filename_field='originalFilename', storage=rcjaRegistration.storageBackends.PrivateMediaStorage(), upload_prefix='MentorFile', verbose_name='File')),
                ('originalFilename', models.CharField(editable=False, max_length=300, verbose_name='Original filename')),
                ('eventAttendance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.BaseEventAttendance', verbose_name='Team/ attendee')),
                ('fileType', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eventfiles.MentorEventFileType', verbose_name='Type')),
                ('uploadedBy', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Uploaded by')),
            ],
            options={
                'verbose_name': 'Mentor Event File Upload',
                'ordering': ['eventAttendance', 'fileType'],
            },
        ),
        migrations.CreateModel(
            name='EventAvailableFileType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('uploadDeadline', models.DateField(verbose_name='Upload deadline')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event', verbose_name='Event')),
                ('fileType', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eventfiles.MentorEventFileType', verbose_name='Type')),
            ],
            options={
                'verbose_name': 'Event Available File Type',
                'ordering': ['event', 'fileType'],
                'unique_together': {('event', 'fileType')},
            },
        ),
    ]