from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from datetime import date
from django.conf import settings
import random
import string

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    # Используем email как уникальный идентификатор
    email = models.EmailField(unique=True)
    public_id = models.CharField(max_length=8, unique=True, editable=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.public_id:
            # Генерируем уникальный ID из 8 символов (заглавные буквы и цифры)
            while True:
                public_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                if not CustomUser.objects.filter(public_id=public_id).exists():
                    self.public_id = public_id
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        try:
            if self.profile.nickname:
                return f"{self.profile.nickname} ({self.username})"
            elif self.profile.first_name and self.profile.last_name:
                return f"{self.profile.first_name} {self.profile.last_name} ({self.username})"
            else:
                return self.username
        except:
            return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    competition_photo = models.ImageField(upload_to='competition_photos/', blank=True, null=True)
    bio = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    birth_year = models.IntegerField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    steam = models.URLField(blank=True, null=True)
    vk = models.URLField(blank=True, null=True)
    is_organizer = models.BooleanField(default=False, verbose_name='Организатор')
    
    def __str__(self):
        return self.user.username


class Organization(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='organization_logos/', blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Организатор'
    )

    def __str__(self):
        return self.name


class Competition(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='competitions')
    name = models.CharField(max_length=255, verbose_name='Название')
    platform = models.CharField(max_length=100, verbose_name='Платформа', default='Virtual')
    description = models.TextField(blank=True, verbose_name='Описание')
    rules = models.TextField(blank=True, verbose_name='Правила проведения')
    start_date = models.DateField(default=date.today, verbose_name='Дата начала')
    end_date = models.DateField(default=date.today, verbose_name='Дата окончания')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    cover = models.ImageField(upload_to='competition_covers/', blank=True, null=True, verbose_name='Обложка')
    leaders = models.ManyToManyField(CustomUser, related_name='leader_competitions', blank=True, verbose_name='Руководители')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'


class Stage(models.Model):
    competition = models.ForeignKey('Competition', on_delete=models.CASCADE, related_name='stages', verbose_name='Соревнование')
    name = models.CharField(max_length=255, verbose_name='Название')
    track_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Название трассы')
    track_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на трассу')
    technical_regulations = models.TextField(blank=True, null=True, verbose_name='Технический регламент')
    tech_reg_file = models.FileField(upload_to='tech_regulations/', blank=True, null=True, verbose_name='Файл технического регламента')
    judging_criteria = models.FileField(upload_to='judging_criteria/', blank=True, null=True, verbose_name='Судейское задание')
    video_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')
    registration_slots = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Количество слотов (0 - без ограничений)')
    registration_start = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name='Начало регистрации')
    registration_end = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name='Окончание регистрации')
    qualification_start = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name='Начало квалификации')
    battles_start = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name='Начало парных заездов')
    
    # Роли пользователей
    judges = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='judging_stages', blank=True, verbose_name='Судьи')
    marshals = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='marshaling_stages', blank=True, verbose_name='Маршалы')
    commentators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='commenting_stages', blank=True, verbose_name='Комментаторы')
    streamers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='streaming_stages', blank=True, verbose_name='Стримеры')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participating_stages', blank=True, verbose_name='Участники')

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.competition.name} - {self.name}"

    class Meta:
        ordering = ['qualification_start']
        verbose_name = 'Этап'
        verbose_name_plural = 'Этапы'


# Логирование на уровне этапа
class StageLog(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='logs')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"[StageLog] {self.action} at {self.timestamp}"


# Логирование на уровне соревнования
class CompetitionLog(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='logs')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"[CompetitionLog] {self.action} at {self.timestamp}"


class QualificationResult(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='qualification_results')
    participant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    attempt_number = models.PositiveIntegerField(default=1)
    score = models.DecimalField(max_digits=5, decimal_places=1)
    angle_score = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    line_score = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    style_score = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    speed_score = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']
        unique_together = ['stage', 'participant', 'attempt_number']

    def __str__(self):
        return f"{self.participant} - {self.score} (Attempt {self.attempt_number})"


class BattleBracket(models.Model):
    BRACKET_TYPES = [
        ('TOP_32', 'Top 32'),
        ('TOP_16', 'Top 16'),
        ('TOP_8', 'Top 8'),
        ('TOP_4', 'Semi-finals'),
        ('TOP_2', 'Finals'),
    ]

    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='battle_brackets')
    bracket_type = models.CharField(max_length=10, choices=BRACKET_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['stage', 'bracket_type']

    def __str__(self):
        return f"{self.stage.name} - {self.get_bracket_type_display()}"


class Battle(models.Model):
    BATTLE_STATES = [
        ('PENDING', 'Ожидает начала'),
        ('IN_PROGRESS', 'В процессе'),
        ('COMPLETED', 'Завершен'),
        ('CANCELLED', 'Отменен'),
    ]

    bracket = models.ForeignKey(BattleBracket, on_delete=models.CASCADE, related_name='battles')
    leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='battle_leads')
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='battle_follows')
    battle_order = models.PositiveIntegerField()
    state = models.CharField(max_length=20, choices=BATTLE_STATES, default='PENDING')
    winner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='battle_wins')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['battle_order']
        unique_together = ['bracket', 'battle_order']

    def __str__(self):
        return f"{self.bracket} - Battle {self.battle_order}: {self.leader} vs {self.follower}"


class BattleRun(models.Model):
    RUN_TYPES = [
        ('LEAD', 'Лидирующий заезд'),
        ('FOLLOW', 'Догоняющий заезд'),
    ]

    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, related_name='runs')
    run_type = models.CharField(max_length=10, choices=RUN_TYPES)
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    angle_score = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    line_score = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    style_score = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    speed_score = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    deductions = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    total_score = models.DecimalField(max_digits=5, decimal_places=1)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['battle', 'run_type']

    def __str__(self):
        return f"{self.battle} - {self.get_run_type_display()}: {self.driver}"


# Глобальное логирование
class GlobalLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"[GlobalLog] {self.action} at {self.timestamp}"
