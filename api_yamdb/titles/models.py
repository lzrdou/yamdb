import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


def current_year():
    """Получение текущего года."""
    return datetime.date.today().year


class Category(models.Model):
    """Категория."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанр."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведение."""

    name = models.TextField()
    year = models.PositiveIntegerField(
        default=current_year(),
        validators=[MinValueValidator(0), MaxValueValidator(current_year())],
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(Genre, through="GenreTitle")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    @property
    def rating(self):
        """Получение среднего значения рейтинга"""
        return self.reviews.aggregate(avg_score=Avg("score"))["avg_score"]


class GenreTitle(models.Model):
    """Модель для связи жанра и произведения."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
