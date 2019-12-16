# Generated by Django 2.2.7 on 2019-12-16 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schools', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('regions', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('name', models.CharField(max_length=20, verbose_name='Name')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='Description')),
                ('state', models.ForeignKey(blank=True, help_text='Blank for global, available to all states', null=True, on_delete=django.db.models.deletion.CASCADE, to='regions.State', verbose_name='State')),
            ],
            options={
                'verbose_name': 'Division',
                'ordering': ['state', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('max_team_members', models.PositiveIntegerField(verbose_name='Max team members')),
                ('startDate', models.DateField(verbose_name='Event start date')),
                ('endDate', models.DateField(verbose_name='Event end date')),
                ('registrationsOpenDate', models.DateField(verbose_name='Registrations open date')),
                ('registrationsCloseDate', models.DateField(verbose_name='Registration close date')),
                ('entryFee', models.PositiveIntegerField(verbose_name='Entry fee')),
                ('location', models.TextField(blank=True, verbose_name='Location')),
                ('compDetails', models.TextField(blank=True, verbose_name='Event details')),
                ('additionalInvoiceMessage', models.TextField(blank=True, verbose_name='Additional invoice message')),
                ('availableDivisions', models.ManyToManyField(blank=True, to='events.Division', verbose_name='Available divisions')),
                ('directEnquiriesTo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Direct enquiries to')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='regions.State', verbose_name='State')),
            ],
            options={
                'verbose_name': 'Event',
                'ordering': ['year', 'state', '-startDate'],
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('purchaseOrderNumber', models.CharField(blank=True, max_length=30, null=True, verbose_name='Purchase order number')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.Event', verbose_name='Event')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='schools.School', verbose_name='School')),
            ],
            options={
                'verbose_name': 'Invoice',
                'ordering': ['event', 'school'],
                'unique_together': {('school', 'event')},
            },
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('year', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='Year')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
            ],
            options={
                'verbose_name': 'Year',
                'ordering': ['-year'],
            },
        ),
        migrations.CreateModel(
            name='InvoicePayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('amountPaid', models.PositiveIntegerField(verbose_name='Amount paid')),
                ('datePaid', models.DateField(verbose_name='Date paid')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.Invoice', verbose_name='Invoice')),
            ],
            options={
                'verbose_name': 'Payment',
                'ordering': ['invoice', 'datePaid'],
            },
        ),
        migrations.AddField(
            model_name='event',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.Year', verbose_name='Year'),
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together={('year', 'state', 'name')},
        ),
    ]
