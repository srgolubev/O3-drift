# Generated by Django 4.2 on 2025-02-08 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_competition_options_competition_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='platform',
            field=models.CharField(default='Windsurfer', max_length=100, verbose_name='Платформа'),
        ),
    ]
