# Generated by Django 5.0.1 on 2024-02-18 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_account_isdeleted_data_log_isdeleted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='accountRole',
            field=models.CharField(blank=True, choices=[('physician', 'Physician'), ('nurse', 'Nurse'), ('admin', 'Admin')], max_length=100),
        ),
    ]