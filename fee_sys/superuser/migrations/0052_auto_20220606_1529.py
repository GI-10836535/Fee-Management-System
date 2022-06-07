# Generated by Django 3.2.13 on 2022-06-06 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0051_invoice_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignpaymentduration',
            name='fee_description',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='superuser.feedescription'),
        ),
        migrations.AddField(
            model_name='invoicedetails',
            name='company_name',
            field=models.CharField(default='Akwaaba Solutions Agency', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='makepayment',
            name='invoice_no',
            field=models.CharField(blank=True, default='FMS2022661', max_length=500, null=True),
        ),
    ]
