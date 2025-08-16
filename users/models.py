from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Кастомный пользователь без явного поля role.
       Роли определяются через группы (Учителя, Ученики)."""
    pass