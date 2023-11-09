# Generated by Django 4.2.3 on 2023-11-06 04:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': 'Account Record', 'verbose_name_plural': 'Account Record'},
        ),
        migrations.AlterModelOptions(
            name='data_log',
            options={'verbose_name': 'Data Logs', 'verbose_name_plural': 'Data Logs'},
        ),
        migrations.AddField(
            model_name='account',
            name='profile_photo',
            field=models.ImageField(blank=True, default=None, upload_to='upload-photo/'),
        ),
        migrations.AddField(
            model_name='account',
            name='token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='data_log',
            name='type',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='personal_note',
            name='isDone',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personal_note',
            name='user',
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name='data_log',
            name='date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='personal_note',
            name='noteNum',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]