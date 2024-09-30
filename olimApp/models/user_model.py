from django.db import models
import uuid
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    """
    Менеджер для модели CustomUser.

    Позволяет создавать пользователей и суперпользователей.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и возвращает пользователя с заданным адресом электронной почты и паролем.

        Аргументы:
            email (str): Адрес электронной почты пользователя.
            password (str): Пароль пользователя.
            **extra_fields: Дополнительные поля для пользователя.

        Исключения:
            ValueError: Если адрес электронной почты не указан.
        """
        if not email:
            raise ValueError("Пользователь должен иметь адрес электронной почты")

        email = self.normalize_email(email)  # Нормализуем адрес электронной почты
        user = self.model(email=email, **extra_fields)  # Создаем пользователя
        user.set_password(password)  # Устанавливаем пароль
        user.save(using=self._db)  # Сохраняем пользователя в базе данных
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и возвращает суперпользователя с заданным адресом электронной почты и паролем.

        Аргументы:
            email (str): Адрес электронной почты суперпользователя.
            password (str): Пароль суперпользователя.
            **extra_fields: Дополнительные поля для суперпользователя.

        Исключения:
            ValueError: Если is_staff или is_superuser не установлены на True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Пользовательская модель пользователя.

    Поля:
        email: Уникальный адрес электронной почты.
        is_active: Статус активности пользователя.
        is_staff: Статус администратора.
        is_superuser: Статус суперпользователя.
        activation_code: Код активации для активации аккаунта.
    """

    email = models.EmailField(unique=True)  # Адрес электронной почты
    is_active = models.BooleanField(default=False)  # Статус активности
    is_staff = models.BooleanField(default=False)  # Статус администратора
    is_superuser = models.BooleanField(default=False)  # Статус суперпользователя
    activation_code = models.UUIDField(default=uuid.uuid4, unique=True, null=True, blank=True)  # Код активации

    objects = CustomUserManager()  # Менеджер для модели

    USERNAME_FIELD = "email"  # Поле, используемое для аутентификации

    def __str__(self):
        """
        Возвращает строковое представление пользователя.

        Возвращает:
            str: Адрес электронной почты пользователя.
        """
        return self.email