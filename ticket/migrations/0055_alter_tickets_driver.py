# Generated by Django 3.2.16 on 2022-11-18 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0054_shuttle_ride_shuttle_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ticket.shuttle_driver'),
        ),
    ]
