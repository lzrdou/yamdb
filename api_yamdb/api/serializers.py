from rest_framework import serializers
from reviews.models import Comment, Review
from titles.models import Category, Genre, Title
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review"""

    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
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
    """Сериализатор модели Category"""

    class Meta:
        model = Category
        fields = ("name", "slug")
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre"""

    class Meta:
        model = Genre
        fields = ("name", "slug")
        lookup_field = "slug"


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title (Post запрос)"""

    description = serializers.CharField(allow_blank=True)
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True, slug_field="slug", queryset=Genre.objects.all()
    )
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = "__all__"


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title (Get запрос)"""

    description = serializers.CharField(allow_blank=True)
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User"""

    class Meta:
        model = User
        fields = (
            "username",
            "role",
            "email",
            "first_name",
            "last_name",
            "bio",
        )


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации"""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError("Имя пользователя не разрешено.")
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена"""

    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)
