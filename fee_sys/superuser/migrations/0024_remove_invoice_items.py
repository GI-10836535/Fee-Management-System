# Generated by Django 4.0.4 on 2022-05-26 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0023_alter_selectedvalue_selected_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='items',
        ),
    ]
