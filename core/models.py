from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
from datetime import date
from django.conf import settings

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
    public_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
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
            self.public_id = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
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
    steam_id = models.CharField(max_length=100, blank=True, null=True)
    vk_id = models.CharField(max_length=100, blank=True, null=True)
    
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
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    name = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='competition_covers/', blank=True, null=True)
    rules = models.TextField(blank=True)
    description = models.TextField(blank=True)
    leaders = models.ManyToManyField(CustomUser, related_name='leader_competitions', blank=True)

    def __str__(self):
        return self.name


class Stage(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='stages')
    name = models.CharField(max_length=255)
    track_name = models.CharField(max_length=255, blank=True, null=True)
    track_link = models.URLField(blank=True, null=True)
    technical_regulation = models.TextField(blank=True, null=True)  # Можно заменить на FileField, если нужен файл
    judge_instruction_file = models.FileField(upload_to='judge_instructions/', blank=True, null=True)
    judge_instruction_video = models.URLField(blank=True, null=True)
    registration_slots = models.PositiveIntegerField(default=0)  # 0 означает без ограничения
    registration_open = models.DateTimeField()
    registration_close = models.DateTimeField()
    qualification_start = models.DateTimeField()
    pair_race_start = models.DateTimeField()
    
    # Роли внутри этапа
    judges = models.ManyToManyField(CustomUser, related_name='judge_stages', blank=True)
    marshals = models.ManyToManyField(CustomUser, related_name='marshal_stages', blank=True)
    commentators = models.ManyToManyField(CustomUser, related_name='commentator_stages', blank=True)
    streamers = models.ManyToManyField(CustomUser, related_name='streamer_stages', blank=True)
    participants = models.ManyToManyField(CustomUser, related_name='participant_stages', blank=True)

    def __str__(self):
        return f"Stage: {self.name} of Competition: {self.competition.name}"


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


# Глобальное логирование
class GlobalLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"[GlobalLog] {self.action} at {self.timestamp}"
