# Generated by Django 4.1.7 on 2023-03-12 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Loyalty_program_app', '0007_alter_invoiceproductslist_qty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]