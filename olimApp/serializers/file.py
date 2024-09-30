from rest_framework import serializers
from ..models import File


class FileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления файлов.

    Позволяет сериализовать данные модели File и предоставляет дополнительное поле для удаления.

    Поля:
        id: Идентификатор файла.
        _destroy: Логическое поле для указания на необходимость удаления файла (необязательное).
    """

    id = serializers.IntegerField()  # Идентификатор файла
    _destroy = serializers.BooleanField(
        required=False, default=False
    )  # Дополнительное поле для удаления файла

    class Meta:
        model = File  # Модель, с которой связан сериализатор
        fields = ["id", "_destroy"]  # Поля, которые будут сериализованы


class FileReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения данных файла.

    Позволяет сериализовать данные модели File для представления пользователям.

    Поля:
        id: Идентификатор файла.
        name: Название файла.
        file: Файл, загруженный пользователем.
        uploaded_at: Дата и время загрузки файла.
    """

    class Meta:
        model = File  # Модель, с которой связан сериализатор
        fields = [
            "id",          # Идентификатор файла
            "name",        # Название файла
            "file",        # Файл, загруженный пользователем
            "uploaded_at", # Дата и время загрузки
        ]