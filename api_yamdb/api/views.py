from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from api_yamdb.settings import ADMIN_EMAIL

from reviews.models import Review
from titles.models import Category, Genre, Title
from users.models import User

from .filters import TitleFilter
from .permissions import (
    AdminPermission,
    AdminSafeMethodsPermission,
    ReviewOwnerPermission,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    TokenSerializer,
    UserSerializer,
)


class ReviewViewSet(viewsets.ModelViewSet):
    """ВьюСет модель для Review."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewOwnerPermission]

    def get_queryset(self):
        """Object's filter."""
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Perform_create для ReviewViewSet (api, author=request.user)."""
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """ВьюСет модель для Comment."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewOwnerPermission]

    def get_queryset(self):
        """Object's filter."""
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        """Perform_create для CommentViewSet (author=request.user)."""
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title=self.kwargs.get("title_id"),
        )
        serializer.save(author=self.request.user, review=review)


class CategoryGenreParentViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Родительский ВьюСет для Category и Genre."""

    lookup_field = "slug"
    permission_classes = [AdminSafeMethodsPermission]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class CategoryViewSet(CategoryGenreParentViewSet):
    """ВьюСет модель для Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreParentViewSet):
    """ВьюСет модель для Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """ВьюСет модель для Title."""

    queryset = Title.objects.all()
    permission_classes = [AdminSafeMethodsPermission]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return TitleGetSerializer
        return TitlePostSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ВьюСет модель для User."""

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
    serializer.is_valid(raise_exception=True)
    username = serializer.data["username"]
    email = serializer.data["email"]
    user = get_object_or_404(User, username=username, email=email)
    send_confirmation_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


def send_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    subject = "Код подтверждения"
    message = f"Ваш код подтверждения: {confirmation_code}"
    admin_email = ADMIN_EMAIL
    user_email = [user.email]
    return send_mail(subject, message, admin_email, user_email)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_user_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data["username"]
    confirmation_code = serializer.data["confirmation_code"]

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(
            "Пользователь не найден", status=status.HTTP_404_NOT_FOUND
        )

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
    serializer.is_valid(raise_exception=True)
    username = serializer.data["username"]
    email = serializer.data["email"]
    user, created = User.objects.get_or_create(username=username, email=email)
    send_confirmation_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
