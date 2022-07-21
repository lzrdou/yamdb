"""Admin in rewiews app"""

from django.contrib import admin

from .models import Review, Comment


class ReviewAdmin(admin.ModelAdmin):
    """Админ модель Review"""

    list_display = (
        "title",
        "text",
        "author",
        "score",
        "pub_date",
    )
    search_fields = (
        "title",
        "text",
        "score",
    )


class CommentAdmin(admin.ModelAdmin):
    """Админ модель Commen"""

    list_display = ("review", "text", "author", "pub_date")
    search_fields = ("review", "text")


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
