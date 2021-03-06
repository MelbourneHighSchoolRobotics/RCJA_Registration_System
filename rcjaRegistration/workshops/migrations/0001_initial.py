# Generated by Django 3.0.3 on 2020-03-14 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0010_auto_20200315_0011'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkshopAttendee',
            fields=[
                ('baseeventattendance_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='events.BaseEventAttendance')),
                ('attendeeType', models.CharField(choices=[('teacher', 'Teacher'), ('student', 'Student')], max_length=15, verbose_name='Attendee type')),
                ('firstName', models.CharField(max_length=50, verbose_name='First name')),
                ('lastName', models.CharField(max_length=50, verbose_name='Last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('yearLevel', models.PositiveIntegerField(blank=True, null=True, verbose_name='Year level')),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10, verbose_name='Gender')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Birthday')),
            ],
            options={
                'verbose_name': 'Workshop attendee',
                'ordering': ['event', 'school', 'division', 'lastName'],
            },
            bases=('events.baseeventattendance',),
        ),
    ]
