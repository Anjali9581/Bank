# Generated by Django 5.1.3 on 2024-12-27 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_bank_aadhar_number_alter_bank_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bank',
            old_name='Aadhar_number',
            new_name='bank_number',
        ),
    ]
