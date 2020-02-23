# Generated by Django 2.2.8 on 2020-02-22 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_invoiceglobalsettings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoiceglobalsettings',
            name='invoiceFromAddress',
        ),
        migrations.AddField(
            model_name='invoiceglobalsettings',
            name='invoiceFromDetails',
            field=models.TextField(default='', verbose_name='Invoice from details'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoiceglobalsettings',
            name='invoiceFromName',
            field=models.CharField(max_length=50, verbose_name='Invoice from name'),
        ),
    ]
