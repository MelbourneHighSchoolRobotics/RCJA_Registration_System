# Generated by Django 2.2.8 on 2020-02-22 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceGlobalSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('invoiceFromName', models.CharField(max_length=50, verbose_name='Invoice name')),
                ('invoiceFromAddress', models.TextField(verbose_name='Invoice address')),
            ],
            options={
                'verbose_name': 'Invoice settings',
            },
        ),
    ]