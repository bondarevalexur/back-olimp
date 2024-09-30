from rest_framework import serializers
from ..models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания пользователей.

    Позволяет сериализовать данные модели CustomUser, включая поля email и password.

    Поля:
        email: Адрес электронной почты пользователя.
        password: Пароль пользователя.
    """

    class Meta:
        model = CustomUser  # Модель, с которой связан сериализатор
        fields = ("email", "password")  # Поля, которые будут сериализованы

    def create(self, validated_data):
        """
        Создает новый объект CustomUser.

        Аргументы:
            validated_data: Словарь с данными пользователя, включая email и пароль.

        Возвращает:
            Созданный объект CustomUser.
        """
        user = CustomUser(
            email=validated_data["email"],
            is_active=False  # Устанавливаем пользователя в неактивный статус по умолчанию
        )

        user.set_password(validated_data["password"])  # Хешируем пароль перед сохранением
        user.save()  # Сохраняем пользователя в базе данных
        return user  # Возвращаем созданного пользователя