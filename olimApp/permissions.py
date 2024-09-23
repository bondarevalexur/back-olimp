from rest_framework import permissions


class CreateUserOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет создаваться всем пользователям
    """

    def has_permission(self, request, view):
        # Разрешить доступ к методу GET (чтение) для всех пользователей
        if request.method in ["POST"]:
            return True

        # Разрешить доступ к другим методам (POST, PUT, DELETE) только администраторам
        return request.user and request.user.is_staff
