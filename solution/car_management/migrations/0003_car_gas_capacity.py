# Generated by Django 3.1 on 2020-08-20 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_management', '0002_auto_20200820_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='gas_capacity',
            field=models.IntegerField(default=50, verbose_name='Gas capacity in Liters'),
        ),
    ]
