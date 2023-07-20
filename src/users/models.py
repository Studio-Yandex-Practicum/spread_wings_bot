from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = "main_admin"
REGION_ADMIN = "region_admin"

ROLES = (
    (ADMIN, "Администратор"),
    (REGION_ADMIN, "Региональный администратор"),
)


class User(AbstractUser):
    """User's model."""

    first_name = models.CharField(
        max_length=50, verbose_name="Имя пользователя"
    )
    last_name = models.CharField(
        max_length=50, verbose_name="Фамилия пользователя"
    )
    username = models.CharField(
        max_length=150, verbose_name="Ник пользователя", null=True
    )
    email = models.EmailField(
        unique=True, verbose_name="Адрес электронной почты"
    )
    role = models.CharField(
        max_length=12,
        choices=ROLES,
        default="region_admin",
        verbose_name="Роль пользователя",
    )
    # TODO: add Region model into django
    # region = other_models.ForeignKey(
    #     Region,
    #     on_delete=other_models.SET_NULL,
    #     null=True,
    #     verbose_name="Регион пользователя"
    # )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.role}"
