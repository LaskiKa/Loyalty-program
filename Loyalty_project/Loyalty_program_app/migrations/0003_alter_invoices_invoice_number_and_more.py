# Generated by Django 4.1.7 on 2023-03-05 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Loyalty_program_app', '0002_userprofile_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoices',
            name='invoice_number',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='invoices',
            name='sale_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='invoices',
            name='vendor',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
