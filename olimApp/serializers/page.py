from rest_framework import serializers
from ..models import Page
from .file import FileSerializer, FileReadSerializer


class PageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления страниц.

    Позволяет сериализовать данные модели Page, включая файлы, связанные с страницей.

    Поля:
        id: Идентификатор страницы.
        title: Заголовок страницы.
        content: Содержимое страницы.
        slug: Уникальный идентификатор для страницы.
        files: Список файлов, связанных со страницей.
    """

    files = FileSerializer(many=True, required=False)  # Список файлов (необязательное поле)

    class Meta:
        model = Page  # Модель, с которой связан сериализатор
        fields = ["id", "title", "content", "slug", "files"]  # Поля, которые будут сериализованы

    def update(self, instance, validated_data):
        """
        Обновляет существующий объект Page, включая связанные файлы.

        Аргументы:
            instance: Объект Page, который необходимо обновить.
            validated_data: Словарь с обновленными данными.

        Возвращает:
            Обновленный объект Page.
        """
        files_data = validated_data.pop("files", [])  # Извлекаем данные файлов, если они есть
        instance = super().update(instance, validated_data)  # Обновляем объект

        # Обработка связанных файлов
        for file_data in files_data:
            if file_data.get("_destroy", False):  # Если поле _destroy установлено в True
                instance.files.remove(file_data["id"])  # Удаляем файл
            else:
                instance.files.add(file_data["id"])  # Добавляем файл

        return instance


class PageReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения данных страницы.

    Позволяет сериализовать данные модели Page для представления пользователям.

    Поля:
        id: Идентификатор страницы.
        title: Заголовок страницы.
        content: Содержимое страницы.
        slug: Уникальный идентификатор для страницы.
        files: Список файлов, связанных со страницей.
    """

    files = FileReadSerializer(
        many=True, read_only=True
    )  # Вложенный сериализатор для чтения данных файлов

    class Meta:
        model = Page  # Модель, с которой связан сериализатор
        fields = ["id", "title", "content", "slug", "files"]  # Поля, которые будут сериализованы