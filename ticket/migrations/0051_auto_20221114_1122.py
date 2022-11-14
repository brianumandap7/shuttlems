# Generated by Django 3.2.16 on 2022-11-14 03:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0050_shuttle_service_list_driver_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shuttle_service',
            name='driver_name',
        ),
        migrations.RemoveField(
            model_name='shuttle_service',
            name='plate_number',
        ),
        migrations.AlterField(
            model_name='shuttle_service',
            name='shuttle_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ticket.shuttle_service_list'),
        ),
    ]
