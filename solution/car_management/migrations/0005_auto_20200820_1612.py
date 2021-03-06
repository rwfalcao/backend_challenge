# Generated by Django 3.1 on 2020-08-20 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_management', '0004_auto_20200820_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='tyre',
            name='currently_in_use',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tyre',
            name='degradation',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3, verbose_name='Tyre Degradation in %'),
        ),
    ]
