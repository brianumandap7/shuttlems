# Generated by Django 4.0.3 on 2022-11-05 16:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket', '0037_participants_hdf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hdf',
            name='email',
        ),
        migrations.AddField(
            model_name='hdf',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]