# Generated by Django 4.0.4 on 2022-06-04 01:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0047_remove_assignpaymentduration_set_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignpaymentduration',
            name='set_pay_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]