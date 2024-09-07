from rest_framework import viewsets
from .models import Page, File, CustomUser
from .serializers import (
    PageSerializer,
    PageReadSerializer,
    FileReadSerializer,
    CustomUserSerializer,
)
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
    SAFE_METHODS,
)
from .permissions import CreateUserOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [
        CreateUserOnly
    ]  # Только аутентифицированные пользователи могут получить доступ


class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = {"email": user.email, "isAdmin": user.is_superuser}
        return Response(data)


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            # Разрешение на просмотр только зарегестрированныем людям
            return [IsAuthenticated()]
        return [IsAdminUser()]  # Разрешить запись только админу

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PageReadSerializer  # Сериализатор для чтения

        return PageSerializer  # Сериализатор для записи


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileReadSerializer
    permission_classes = [IsAuthenticated]