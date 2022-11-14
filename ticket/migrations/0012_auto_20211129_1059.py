# Generated by Django 3.1.1 on 2021-11-29 02:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket', '0011_auto_20211129_1055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shuttle',
            name='driver',
        ),
        migrations.AddField(
            model_name='stations',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]