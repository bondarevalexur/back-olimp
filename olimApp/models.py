from django.db import models
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и возвращает пользователя с введенными email и паролем.
        """
        if not email:
            raise ValueError("Пользователь должен иметь адрес электронной почты")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Устанавливаем пароль
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и возвращает суперпользователя.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email


class File(models.Model):

    name = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField(
        upload_to="uploads/", null=True, blank=True
    )  # Путь для хранения файлов
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Дата и время загрузки

    def __str__(self):
        return self.file.name


class Page(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    files = models.ManyToManyField(
        File, related_name="pages", blank=True
    )  # Связь многие-ко-многим

    def __str__(self):
        return self.title


@receiver(post_delete, sender=File)
def delete_file_from_filesystem(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
