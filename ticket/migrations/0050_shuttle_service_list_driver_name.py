# Generated by Django 3.2.16 on 2022-11-14 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0049_shuttle_driver_shuttle_service_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='shuttle_service_list',
            name='driver_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ticket.shuttle_driver'),
        ),
    ]
