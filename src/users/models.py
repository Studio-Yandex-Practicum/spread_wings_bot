from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """User's model."""

    class UserRole(models.TextChoices):
        """Supporting model to make Choices field."""

        ADMIN = "main_admin", _("Администратор")
        REGION_ADMIN = "region_admin", _("Региональный администратор")

    username = None
    first_name = models.CharField(
        max_length=50, verbose_name="Имя пользователя"
    )
    last_name = models.CharField(
        max_length=50, verbose_name="Фамилия пользователя"
    )
    email = models.EmailField(
        unique=True, verbose_name="Адрес электронной почты"
    )
    role = models.CharField(
        max_length=12,
        choices=UserRole.choices,
        default=UserRole.REGION_ADMIN,
        verbose_name="Роль пользователя",
    )
    # TODO: add Region model into django
    # region = models.ForeignKey(
    #     Region,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     verbose_name="Регион пользователя"
    # )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.role}"
