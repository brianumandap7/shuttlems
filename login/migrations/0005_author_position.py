# Generated by Django 3.2.16 on 2022-11-09 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_rename_student_number_author_student_or_employee_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='position',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
