import django_filters
from django.db import models
from titles.models import Title


class TitleFilter(django_filters.FilterSet):
    class Meta:
        model = Title
        fields = ["category", "genre", "name", "year"]
        filter_overrides = {
            models.CharField: {
                "filter_class": django_filters.CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            },
            models.SlugField: {
                "filter_class": django_filters.CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            },
        }
        exclude = ["description"]
