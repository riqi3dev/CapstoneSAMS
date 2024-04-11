# Generated by Django 5.0.1 on 2024-04-11 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_remove_account_suffixtitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='accountRole',
            field=models.CharField(blank=True, choices=[('physician', 'Physician'), ('nurse', 'Nurse'), ('student nurse', 'Student Nurse'), ('admin', 'Admin')], max_length=100),
        ),
    ]
