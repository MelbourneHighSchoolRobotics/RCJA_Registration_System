# Generated by Django 2.2.10 on 2020-02-28 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0003_auto_20200226_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='event',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='events.Event', verbose_name='Event'),
        ),
    ]