# Generated by Django 4.1.7 on 2023-03-18 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Loyalty_program_app', '0015_remove_userprofile_user_nip_invoices_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='nip',
            field=models.IntegerField(default=1),
        ),
    ]
