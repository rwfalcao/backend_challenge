# Generated by Django 3.1 on 2020-08-20 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_management', '0003_car_gas_capacity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='gas_capacity',
            field=models.IntegerField(verbose_name='Gas capacity in Liters'),
        ),
    ]
