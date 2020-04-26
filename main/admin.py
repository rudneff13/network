from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Post, Like, Activity


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active', 'first_name', 'last_name')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')
        }
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'header', 'total_likes')
    fields = ('user', 'header', 'text')
    readonly_fields = ('total_likes',)
    ordering = ('user',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object')
    readonly_fields = ('id', 'timestamp', 'object_id', 'content_object')


@admin.register(Activity)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'activity')
    readonly_fields = ('user', 'date', 'activity')
