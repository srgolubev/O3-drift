# Generated by Django 4.2 on 2025-02-08 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_profile_is_organizer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='public_id',
            field=models.CharField(editable=False, max_length=8, unique=True),
        ),
    ]
