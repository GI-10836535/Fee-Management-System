# Generated by Django 3.2.13 on 2022-06-06 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20220606_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payments',
            name='payers_first_name',
        ),
        migrations.RemoveField(
            model_name='payments',
            name='payers_last_name',
        ),
        migrations.RemoveField(
            model_name='payments',
            name='remarks',
        ),
    ]
