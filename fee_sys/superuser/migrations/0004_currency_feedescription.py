# Generated by Django 4.0.4 on 2022-05-19 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0003_alter_feeitems_fee_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeeDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_description', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
