from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
    SAFE_METHODS,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import send_mail
from rest_framework import status
from pathlib import Path
import environ
import os

from ..models import CustomUser
from ..serializers import (
    CustomUserSerializer,
)

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


class CustomUserViewSet(APIView):
    """
    ViewSet для управления пользователями.

    Позволяет регистрировать пользователей и изменять их пароли.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Установка разрешений на основе метода запроса.

        Возвращает:
            - AllowAny, если метод - POST (для регистрации)
            - IsAuthenticated для всех других методов
        """
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def post(self, request):
        """
        Регистрация нового пользователя.

        Параметры запроса:
            - email: str - адрес электронной почты пользователя
            - password: str - пароль пользователя

        Возвращает:
            - сообщение об успешной регистрации и запросе на активацию по электронной почте
            - ошибки валидации, если есть
        """
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            self.send_activation_email(user)
            return Response({"message": "Пользователь успешно зарегистрирован! Проверьте свою почту для активации."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        Изменение пароля пользователя.

        Параметры запроса:
            - last_password: str - текущий пароль
            - new_password: str - новый пароль

        Возвращает:
            - сообщение об успешном изменении пароля
            - ошибку, если текущий пароль неверный
        """
        user = request.user
        last_password = request.data["last_password"]
        new_password = request.data["new_password"]

        if not user.check_password(last_password):
            return Response({"message": "Неверный пароль "}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Пароль успешно изменен"}, status=status.HTTP_200_OK)

    def send_activation_email(self, user):
        print(env('DEFAULT_FROM_EMAIL'),user)
        """
        Отправка электронного письма для активации аккаунта.

        Параметры:
            - user: CustomUser - объект пользователя, которому отправляется письмо
        """
        activation_code = user.activation_code
        html_message = render_to_string('code_mail.html', {'user': user, 'activation_code': activation_code})
        plain_message = strip_tags(html_message)
        subject = 'Активация аккаунта'
        from_email = "admin@math-championship.ru"
        to = user.email
        print(to)
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)


class ActivateProfileView(APIView):
    """
    View для активации профиля пользователя по коду активации.
    """

    def get(self, request):
        """
        Активация аккаунта пользователя.

        Параметры запроса:
            - activation_code: str - код активации

        Возвращает:
            - сообщение об успешной активации
            - ошибку, если код неверный или аккаунт уже активирован
        """
        activation_code = request.query_params.get('activation_code')

        try:
            user = CustomUser.objects.get(activation_code=activation_code)
        except CustomUser.DoesNotExist:
            return Response({"error": "Неверный код активации"}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({"message": "Аккаунт уже активирован."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.activation_code = None  # Очищаем код после активации
        user.save()

        return Response({"message": "Аккаунт успешно активирован!"}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    """
    View для получения профиля пользователя.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Получение информации о пользователе.

        Возвращает:
            - email: str - адрес электронной почты пользователя
            - isAdmin: bool - статус администратора
            - isActive: bool - статус активации
        """
        user = request.user
        data = {"email": user.email, "isAdmin": user.is_superuser, "isActive": user.is_active}
        return Response(data)
