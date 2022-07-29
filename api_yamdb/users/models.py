from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    USER_ROLE = [
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    bio = models.CharField(max_length=200, blank=True, null=True)
    role = models.CharField(
        choices=USER_ROLE, max_length=9, blank=True, null=True, default=USER
    )
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=254, default="")
    last_login = models.DateTimeField(auto_now_add=True)

    @property
    def is_user(self):
        return self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
