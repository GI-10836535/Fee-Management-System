# Generated by Django 4.0.4 on 2022-05-24 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0021_invoice_items_invoice_total_amount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelectedValue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('selected_value', models.IntegerField(default=0)),
            ],
        ),
    ]
