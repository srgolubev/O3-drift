# Generated by Django 4.2 on 2025-02-08 21:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_competition_platform'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stage',
            options={'ordering': ['qualification_start'], 'verbose_name': 'Этап', 'verbose_name_plural': 'Этапы'},
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_organizer',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='judge_instruction_file',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='judge_instruction_video',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='pair_race_start',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='registration_close',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='registration_open',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='technical_regulation',
        ),
        migrations.AddField(
            model_name='stage',
            name='battles_start',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Начало парных заездов'),
        ),
        migrations.AddField(
            model_name='stage',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='stage',
            name='judging_criteria',
            field=models.FileField(blank=True, null=True, upload_to='judging_criteria/', verbose_name='Судейское задание'),
        ),
        migrations.AddField(
            model_name='stage',
            name='registration_end',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Окончание регистрации'),
        ),
        migrations.AddField(
            model_name='stage',
            name='registration_start',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Начало регистрации'),
        ),
        migrations.AddField(
            model_name='stage',
            name='tech_reg_file',
            field=models.FileField(blank=True, null=True, upload_to='tech_regulations/', verbose_name='Файл технического регламента'),
        ),
        migrations.AddField(
            model_name='stage',
            name='technical_regulations',
            field=models.TextField(blank=True, null=True, verbose_name='Технический регламент'),
        ),
        migrations.AddField(
            model_name='stage',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='stage',
            name='video_link',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на видео'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='competition_covers/', verbose_name='Обложка'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='competition',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='leaders',
            field=models.ManyToManyField(blank=True, related_name='leader_competitions', to=settings.AUTH_USER_MODEL, verbose_name='Руководители'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='rules',
            field=models.TextField(blank=True, verbose_name='Правила проведения'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='biography',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='competition_photo',
            field=models.ImageField(blank=True, null=True, upload_to='competition_photos/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='steam',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='vk',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stage',
            name='commentators',
            field=models.ManyToManyField(blank=True, related_name='commenting_stages', to=settings.AUTH_USER_MODEL, verbose_name='Комментаторы'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='competition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stages', to='core.competition', verbose_name='Соревнование'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='judges',
            field=models.ManyToManyField(blank=True, related_name='judging_stages', to=settings.AUTH_USER_MODEL, verbose_name='Судьи'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='marshals',
            field=models.ManyToManyField(blank=True, related_name='marshaling_stages', to=settings.AUTH_USER_MODEL, verbose_name='Маршалы'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participating_stages', to=settings.AUTH_USER_MODEL, verbose_name='Участники'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='qualification_start',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Начало квалификации'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='registration_slots',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Количество слотов (0 - без ограничений)'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='streamers',
            field=models.ManyToManyField(blank=True, related_name='streaming_stages', to=settings.AUTH_USER_MODEL, verbose_name='Стримеры'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='track_link',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на трассу'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='track_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название трассы'),
        ),
    ]
