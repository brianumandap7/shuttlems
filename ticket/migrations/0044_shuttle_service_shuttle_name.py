# Generated by Django 3.2.16 on 2022-11-09 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0043_rename_shuttle_url_shuttle_service_gps_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='shuttle_service',
            name='shuttle_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
