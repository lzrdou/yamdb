"""Models from reviews app (api_yamdb)."""

from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator

from users.models import User
from titles.models import Title

text_for_view = 25  # a slice for displaying text


class Review(models.Model):
    """Model Review from reviews app."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.PositiveIntegerField(
        default=5, validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        "Дата публикации отзыва", auto_now_add=True
    )

    class Meta:
        """Class Meta for model Review"""

        constraints = [
            models.UniqueConstraint(  # One review of the author to title
                fields=["author", "title"], name="unique_review"
            )
        ]

    def __str__(self):
        return self.text[:text_for_view]


class Comment(models.Model):
    """Model Comments from reviews app."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        blank=True,
        null=True,
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField(
        "Дата публикации комментария", auto_now_add=True
    )

    def __str__(self):
        return self.text[:text_for_view]
