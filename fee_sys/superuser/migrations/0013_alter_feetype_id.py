# Generated by Django 4.0.4 on 2022-05-19 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0012_alter_feeitems_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feetype',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
