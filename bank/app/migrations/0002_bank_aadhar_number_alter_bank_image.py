# Generated by Django 5.1.3 on 2024-12-27 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='Aadhar_number',
            field=models.IntegerField(default=123456789001, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bank',
            name='image',
            field=models.ImageField(upload_to='profile'),
        ),
    ]