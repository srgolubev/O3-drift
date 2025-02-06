from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Organization, Competition, Stage, StageLog, CompetitionLog, GlobalLog


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'public_id', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'public_id')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'first_name', 'last_name', 'vk_id', 'steam_id')
    search_fields = ('user__username', 'nickname', 'first_name', 'last_name')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'organizer')
    search_fields = ('name', 'abbreviation')


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization')
    search_fields = ('name', 'organization__name')


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'competition', 'registration_open', 'registration_close')
    search_fields = ('name', 'competition__name')
    list_filter = ('registration_open', 'registration_close')


@admin.register(StageLog)
class StageLogAdmin(admin.ModelAdmin):
    list_display = ('stage', 'action', 'timestamp', 'user')
    search_fields = ('stage__name', 'action')


@admin.register(CompetitionLog)
class CompetitionLogAdmin(admin.ModelAdmin):
    list_display = ('competition', 'action', 'timestamp', 'user')
    search_fields = ('competition__name', 'action')


@admin.register(GlobalLog)
class GlobalLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'timestamp', 'user')
    search_fields = ('action', 'user__username')
