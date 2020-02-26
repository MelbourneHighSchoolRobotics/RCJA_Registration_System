# Generated by Django 2.2.10 on 2020-02-26 03:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userquestions', '0002_auto_20200226_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDateTime', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updatedDateTime', models.DateTimeField(auto_now=True, verbose_name='Last modified date')),
                ('response', models.BooleanField(verbose_name='Response')),
            ],
            options={
                'verbose_name': 'User Question Response',
                'ordering': ['question', 'user'],
            },
        ),
        migrations.RenameModel(
            old_name='UserQuestion',
            new_name='Question',
        ),
        migrations.DeleteModel(
            name='UserQuestionResponse',
        ),
        migrations.AddField(
            model_name='questionresponse',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userquestions.Question', verbose_name='Question'),
        ),
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
