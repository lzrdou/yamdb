from rest_framework import serializers

from reviews.models import Review, Comment

# from titles.models import Category, Genre, Title
# from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review"""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment"""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")


class CategorySerializer(serializers.ModelSerializer):
    pass


class GenreSerializer(serializers.ModelSerializer):
    pass


class TitleSerializer(serializers.ModelSerializer):
    pass


class UserSerializer(serializers.ModelSerializer):
    pass
