# Generated by Django 4.2 on 2025-02-08 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_stage_options_remove_profile_is_admin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_organizer',
            field=models.BooleanField(default=False, verbose_name='Организатор'),
        ),
    ]
