# Generated by Django 4.2.3 on 2023-07-23 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_bulk_drug_options_remove_bulk_drug_bnf_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bulk_drug',
            options={'ordering': ['bnf']},
        ),
        migrations.AddField(
            model_name='bulk_drug',
            name='bnf',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='bulk_drug',
            name='description',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='bulk_drug',
            name='csv',
            field=models.FileField(blank=True, upload_to='csv/'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')]),
        ),
    ]