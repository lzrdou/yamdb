from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "bio", "role")
    search_fields = ("username",)
    list_filter = ("role",)
