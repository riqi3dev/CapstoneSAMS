# Generated by Django 4.2.3 on 2023-07-23 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_remove_bulk_drug_csv_alter_patient_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male')]),
        ),
    ]