# Generated by Django 2.2.10 on 2020-02-25 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0011_invoiceglobalsettings_invoicefootermessage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ['-invoiceNumber'], 'verbose_name': 'Invoice'},
        ),
    ]