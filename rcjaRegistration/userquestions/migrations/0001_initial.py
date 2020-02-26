# Generated by Django 2.2.10 on 2020-02-26 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('questionText', models.TextField(verbose_name='Question text')),
                ('required', models.BooleanField(default=True, help_text='Users must accept required questions to register', verbose_name='Required')),
            ],
            options={
                'verbose_name': 'User Question',
                'ordering': ['-creationDateTime'],
            },
        ),
        migrations.CreateModel(
            name='UserQuestionResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('response', models.BooleanField(verbose_name='Response')),
            ],
            options={
                'verbose_name': 'User Question Response',
                'ordering': ['userQuestion', 'user'],
            },
        ),
    ]
