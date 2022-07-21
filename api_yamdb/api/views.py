import uuid
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from .permissions import AdminPermission

from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import send_mail
from rest_framework.decorators import api_view

# from reviews.models import Review, Comment
# from titles.models import Category, Genre, Title
from users.models import User
from serializers import (
    UserSerializer,
    ConfirmationCodeSerializer,
    UserEmailSerializer,
)

#     ReviewSerializer,
#     CommentSerializer,
#     CategorySerializer,
#     GenreSerializer,
#     TitleSerializer,


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    pass


class GenreViewSet(viewsets.ModelViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)


@api_view(["POST"])
def send_confirmation_code(request):
    serializer = UserEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.data["email"]
    user_is_exist = User.objects.filter(email=email).exists()
    if not user_is_exist:
        User.objects.create_user(username=email, email=email)

    confirmation_code = uuid.uuid3(uuid.NAMESPACE_DNS, email)

    send_mail(
        "Код подтверждения",
        f"Ваш код подтверждения: {confirmation_code}",
        "admin@admin.com",
        [email],
        fail_silently=False,
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_user_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.data["email"]
    confirmation_code = serializer.data["confirmation_code"]

    user = get_object_or_404(User, email=email)
    code = str(uuid.uuid3(uuid.NAMESPACE_DNS, email))
    if code != confirmation_code:
        return Response(
            {"confirmation_code": "Неверный код"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    token = AccessToken.for_users(user)

    return Response({f"token: {token}"}, status=status.HTTP_200_OK)
