# Generated by Django 3.1.1 on 2021-12-09 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0025_auto_20211209_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hdf',
            name='user',
        ),
        migrations.AddField(
            model_name='hdf',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]