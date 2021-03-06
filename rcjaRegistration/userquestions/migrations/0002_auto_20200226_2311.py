# Generated by Django 2.2.10 on 2020-02-26 12:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userquestions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionresponse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterUniqueTogether(
            name='questionresponse',
            unique_together={('question', 'user')},
        ),
    ]
