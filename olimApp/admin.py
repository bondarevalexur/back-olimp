from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Админ-класс для модели CustomUser.

    Позволяет управлять пользователями через админ-панель Django.
    """

    model = CustomUser  # Модель, которую будет использовать админ-класс
    list_display = ["email", "is_staff"]  # Поля, отображаемые в списке пользователей
    ordering = ["email"]  # Сортировка списка пользователей по адресу электронной почты

    fieldsets = (
        (None, {"fields": ("email", "password")}),  # Основные поля пользователя
        ("Permissions", {"fields": ("is_active", "activation_code", "is_staff", "is_superuser")}),  # Права доступа
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),  # Класс для отображения полей
                "fields": (
                    "email",
                    "password1",  # Пароль при создании пользователя
                    "is_active",  # Статус активности
                    "is_staff",  # Статус администратора
                    "is_superuser",  # Статус суперпользователя
                    "activation_code",  # Код активации
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)  # Регистрация модели в админ-панели