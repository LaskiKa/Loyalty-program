# Generated by Django 4.1.7 on 2023-03-18 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Loyalty_program_app', '0017_alter_userprofile_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='points',
            field=models.IntegerField(default=0, max_length=10000),
        ),
    ]
