from rest_framework import viewsets
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
    SAFE_METHODS,
)

from ..models import Page
from ..serializers import (
    PageSerializer,
    PageReadSerializer
)


class PageViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления страницами.

    Позволяет выполнять операции создания, чтения, обновления и удаления страниц.
    """

    queryset = Page.objects.all()

    def get_permissions(self):
        """
        Устанавливает разрешения на основе метода запроса.

        Возвращает:
            - IsAuthenticated: если метод безопасный (GET, HEAD, OPTIONS)
            - IsAdminUser: если метод не безопасный (POST, PUT, PATCH, DELETE)
        """
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]  # Доступ к безопасным методам для аутентифицированных пользователей
        return [IsAdminUser()]  # Доступ к не безопасным методам только для администраторов

    def get_serializer_class(self):
        """
        Определяет, какой сериализатор использовать на основе действия.

        Возвращает:
            - PageReadSerializer: для действий чтения (list, retrieve)
            - PageSerializer: для действий записи (create, update, delete)
        """
        if self.action in ["list", "retrieve"]:
            return PageReadSerializer  # Используется для чтения данных страницы
        return PageSerializer  # Используется для записи данных страницы