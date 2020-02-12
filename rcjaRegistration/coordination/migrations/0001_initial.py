# Generated by Django 2.2.8 on 2020-01-04 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('regions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('permissions', models.CharField(choices=[('readonly', 'Read only'), ('full', 'Full')], max_length=20, verbose_name='Permissions')),
                ('position', models.CharField(max_length=50, verbose_name='Position')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='regions.State', verbose_name='State')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Coordinator',
                'ordering': ['state', 'user'],
                'unique_together': {('user', 'state')},
            },
        ),
    ]