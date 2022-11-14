# Generated by Django 3.1.1 on 2021-09-19 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracing', '0003_auto_20210919_2310'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_tracing',
            name='body_pain',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='contact_tracing',
            name='cold',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='contact_tracing',
            name='headache',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='contact_tracing',
            name='loss_of_smell',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='contact_tracing',
            name='loss_of_taste',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='contact_tracing',
            name='fever',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Choices',
        ),
    ]
