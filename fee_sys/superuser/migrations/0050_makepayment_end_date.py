# Generated by Django 3.2.13 on 2022-06-04 05:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0049_makepayment_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='makepayment',
            name='end_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
