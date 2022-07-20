from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    ReviewViewSet,
    CommentViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet,
)

app_name = "api"

router = SimpleRouter()

router.register("categories", CategoryViewSet, basename="categories")

router.register("genres", GenreViewSet, basename="genres")

router.register("titles", TitleViewSet, basename="titles")

router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)

router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

router.register("auth", UserViewSet, basename="auth")

urlpatterns = [
    path("v1/", include(router.urls)),
]
