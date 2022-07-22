from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    USER_ROLE = [
        (USER, "user"),
        (MODERATOR, "moderator"),
        (ADMIN, "admin"),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=100, blank=True)
    role = models.CharField(
        choices=USER_ROLE, max_length=9, blank=True, null=True, default=USER
    )
    password = None

    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

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
