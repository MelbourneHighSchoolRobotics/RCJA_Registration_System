# Generated by Django 2.2.10 on 2020-02-28 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_auto_20200228_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceglobalsettings',
            name='firstInvoiceNumber',
            field=models.PositiveIntegerField(default=1, verbose_name='First invoice number'),
        ),
    ]
