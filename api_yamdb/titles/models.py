from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
import datetime


# Получение текущего года
def current_year():
    return datetime.date.today().year


# Категория
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# Жанр
class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# Произведение
class Title(models.Model):
    name = models.CharField(max_length=512)
    year = models.PositiveIntegerField(
        default=current_year(),
        validators=[MinValueValidator(0), MaxValueValidator(current_year())],
    )
    description = models.TextField(max_length=1024)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
    )

    # Получение среднего значения рейтинга
    @property
    def rating(self):
        return self.reviews.aggregate(avg_score=Avg("score"))["avg_score"]
