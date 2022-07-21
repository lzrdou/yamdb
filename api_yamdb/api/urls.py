from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    send_confirmation_code,
    get_user_token,
    ReviewViewSet,
    CommentViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet,
    UserInfo,
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
    path("v1/auth/email/", send_confirmation_code),
    path("v1/auth/token/", get_user_token),
    path("v1/user/me/", UserInfo.as_view()),
    path("v1/", include(router.urls)),
]
