from rest_framework import viewsets
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
    SAFE_METHODS,
)

from ..models import File
from ..serializers import (
    FileReadSerializer
)


class FileViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления файлами.

    Позволяет выполнять CRUD (создание, чтение, обновление и удаление) операции с моделями File.

    Атрибуты:
        queryset: QuerySet для выборки всех файлов.
        serializer_class: Сериализатор для преобразования данных файла.
        permission_classes: Ограничивает доступ к методам ViewSet в зависимости от аутентификации пользователя.
    """

    queryset = File.objects.all()
    serializer_class = FileReadSerializer
    permission_classes = [IsAuthenticated]  # Разрешает доступ только аутентифицированным пользователям

    def get_permissions(self):
        """
        Определяет разрешения для доступа к методам ViewSet на основе метода запроса.

        Возвращает:
            - IsAuthenticated: разрешает доступ только аутентифицированным пользователям
              для всех методов (включая чтение).
        """
        return super().get_permissions()  # В данном случае используются общие разрешения для всех методов