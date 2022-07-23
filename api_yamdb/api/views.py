from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import filters, viewsets, status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework.serializers import ValidationError

from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from rest_framework.decorators import api_view, action, permission_classes

from .permissions import (
    AdminPermission,
    GeneralPermission,
    ReviewOwnerPermission,
)
from reviews.models import Review
from titles.models import Category, Genre, Title
from users.models import User
from .serializers import (
    UserSerializer,
    TokenSerializer,
    SignupSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer,
)


class ReviewViewSet(viewsets.ModelViewSet):
    """ВьюСет модель для Review."""

    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewOwnerPermission]

    def get_queryset(self):
        """Object's filter."""
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Perform_create для ReviewViewSet (api, author=request.user)."""
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        author = self.request.user
        if Review.objects.filter(title=title_id, author=author).exists():
            raise ValidationError("Можно оставить только один отзыв.")
        serializer.save(author=author, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """ВьюСет модель для Comment."""

    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewOwnerPermission]

    def get_queryset(self):
        """Object's filter."""
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        """Perform_create для CommentViewSet (author=request.user)."""
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(viewsets.ModelViewSet):
    """ВьюСет модель для Category."""

    queryset = Category.objects.get_queryset().order_by("id")
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = [GeneralPermission]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class GenreViewSet(viewsets.ModelViewSet):
    """ВьюСет модель для Genre."""

    queryset = Genre.objects.get_queryset().order_by("id")
    serializer_class = GenreSerializer
    lookup_field = "slug"
    permission_classes = [GeneralPermission]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class TitleViewSet(viewsets.ModelViewSet):
    """ВьюСет модель для Title."""

    queryset = Title.objects.get_queryset().order_by("category")
    serializer_class = TitleSerializer
    permission_classes = [GeneralPermission]
    pagination_class = PageNumberPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    filterset_fields = ("category", "genre", "name", "year")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = "username"
    lookup_value_regex = r"[\w\@\.\+\-]+"
    search_fields = ("username",)

    @action(
        methods=["patch", "get"],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == "PATCH":
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def code(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data["username"]
        email = serializer.data["email"]
        user = get_object_or_404(User, username=username, email=email)
        send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    subject = "Код подтверждения"
    message = f"Ваш код подтверждения: {confirmation_code}"
    admin_email = "admin@admin.com"
    user_email = [user.email]
    return send_mail(subject, message, admin_email, user_email)


@api_view(["POST"])
def get_user_token(request):
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.data["username"]
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.data["confirmation_code"]

    if not default_token_generator.check_token(user, confirmation_code):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    token = RefreshToken.for_users(user)
    return Response(
        {token: str(token.access_token)}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
