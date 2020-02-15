# Generated by Django 2.2.8 on 2020-02-11 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0001_initial'),
        ('mentorquestions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentorQuestionResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('response', models.BooleanField(verbose_name='Response')),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.Mentor', verbose_name='Mentor')),
                ('mentorQuestion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorquestions.MentorQuestion', verbose_name='Mentor question')),
            ],
            options={
                'verbose_name': 'Mentor Question Response',
                'ordering': ['mentorQuestion'],
            },
        ),
    ]
