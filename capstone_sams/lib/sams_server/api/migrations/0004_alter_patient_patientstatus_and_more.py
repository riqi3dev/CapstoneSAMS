# Generated by Django 5.0.1 on 2024-02-06 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_patient_patientstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='patientStatus',
            field=models.CharField(choices=[('Separated', 'Separated'), ('Divorced', 'Divorced'), ('Single', 'Single'), ('Married', 'Married'), ('Widowed', 'Widowed')]),
        ),
        migrations.AlterField(
            model_name='present_illness',
            name='updated_at',
            field=models.DateTimeField(default=None),
        ),
    ]
