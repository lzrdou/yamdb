from django.contrib import admin

from .models import Category, Genre, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "title")


class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "title")


class TitleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "year", "description", "genre", "category")
    search_fields = ("name", "year", "genre", "category")
    list_filter = (
        "id",
        "year",
    )
    empty_value_field = "-пусто-"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
