# Generated by Django 4.0.3 on 2022-10-25 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0032_ticket_status_remove_tickets_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='ticket_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ticket.ticket_status'),
        ),
    ]
