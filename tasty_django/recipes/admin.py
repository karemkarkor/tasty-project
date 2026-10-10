from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Recipe, Favorite


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Extends the default UserAdmin to show our custom user_type field.
    """
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role', {'fields': ('user_type',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role', {'fields': ('user_type',)}),
    )
    list_display = ('username', 'email', 'user_type', 'is_staff', 'date_joined')
    list_filter = ('user_type', 'is_staff', 'is_active')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'cook_time')
    list_filter = ('type',)
    search_fields = ('title', 'description')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'added_at')
