# Generated by Django 3.2.16 on 2022-11-09 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0044_shuttle_service_shuttle_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shuttle_service',
            old_name='driver',
            new_name='driver_name',
        ),
    ]
