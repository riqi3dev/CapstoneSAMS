# Generated by Django 5.0.1 on 2024-04-01 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_account_accountrole'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='suffixTitle',
        ),
    ]
