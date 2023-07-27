# Generated by Django 4.2.3 on 2023-07-27 00:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_personal_note_isdone_alter_personal_note_notenum'),
    ]

    operations = [
        migrations.AddField(
            model_name='data_log',
            name='type',
            field=models.CharField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personal_note',
            name='user',
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name='data_log',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
