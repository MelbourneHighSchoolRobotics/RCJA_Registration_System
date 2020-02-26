# Generated by Django 2.2.10 on 2020-02-26 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Name')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Region',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Name')),
                ('abbreviation', models.CharField(max_length=3, unique=True, verbose_name='Abbreviation')),
                ('bankAccountName', models.CharField(blank=True, max_length=200, null=True, verbose_name='Bank Account Name')),
                ('bankAccountBSB', models.CharField(blank=True, max_length=7, null=True, verbose_name='Bank Account BSB')),
                ('bankAccountNumber', models.CharField(blank=True, max_length=10, null=True, verbose_name='Bank Account Number')),
                ('paypalEmail', models.EmailField(blank=True, max_length=254, verbose_name='PayPal email')),
                ('defaultEventDetails', models.TextField(blank=True, verbose_name='Default event details')),
                ('invoiceMessage', models.TextField(blank=True, verbose_name='Invoice message')),
            ],
            options={
                'verbose_name': 'State',
                'ordering': ['name'],
            },
        ),
    ]
