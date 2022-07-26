from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    code,
    get_user_token,
    signup,
)

app_name = "api"

router = SimpleRouter()

router.register("categories", CategoryViewSet, basename="categories")

router.register("genres", GenreViewSet, basename="genres")

router.register("titles", TitleViewSet, basename="titles")

router.register("users", UserViewSet, basename="users")

router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)

router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("v1/auth/code/", code),
    path("v1/auth/token/", get_user_token),
    path("v1/auth/signup/", signup),
    path("v1/", include(router.urls)),
]
