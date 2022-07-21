from rest_framework import viewsets
from django.shortcuts import get_object_or_404

# from reviews.models import Review, Comment
# from titles.models import Category, Genre, Title
# from users.models import User
from serializers import ReviewSerializer, CommentSerializer
from titles.models import Title
from reviews.models import Review

# from serializers import (
#     ReviewSerializer,
#     CommentSerializer,
#     CategorySerializer,
#     GenreSerializer,
#     TitleSerializer,
#     UserSerializer,
# )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    #   permission_classes =

    def get_queryset(self):
        """Object's filter."""
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Perform_create для ReviewViewSe (api, author=request.user)."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Object's filter."""
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        """Perform_create для CommentViewSet (author=request.user)."""
        serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    pass


class GenreViewSet(viewsets.ModelViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    pass
