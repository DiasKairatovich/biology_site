from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Кастомная модель пользователя с дополнительными полями."""

    ROLE_CHOICES = [
        ("student", "Ученик"),
        ("teacher", "Учитель"),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="student",
        verbose_name="Роль"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="О себе"
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар"
    )

    def __str__(self):
        # Если есть имя, показываем его, иначе username
        full_name = self.get_full_name() or self.username
        return f"{full_name} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"