# Generated by Django 3.1 on 2020-08-20 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car_management', '0006_auto_20200820_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_management.trip'),
        ),
    ]
