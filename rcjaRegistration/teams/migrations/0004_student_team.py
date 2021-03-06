# Generated by Django 3.0.3 on 2020-03-14 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0009_baseeventattendance'),
        ('teams', '0003_auto_20200314_2341'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('baseeventattendance_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='events.BaseEventAttendance')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Team',
                'ordering': ['event', 'school', 'division', 'name'],
            },
            bases=('events.baseeventattendance',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('firstName', models.CharField(max_length=50, verbose_name='First name')),
                ('lastName', models.CharField(max_length=50, verbose_name='Last name')),
                ('yearLevel', models.PositiveIntegerField(verbose_name='Year level')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10, verbose_name='Gender')),
                ('birthday', models.DateField(verbose_name='Birthday')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.Team', verbose_name='Team')),
            ],
            options={
                'verbose_name': 'Student',
                'ordering': ['team', 'lastName', 'firstName'],
            },
        ),
    ]
