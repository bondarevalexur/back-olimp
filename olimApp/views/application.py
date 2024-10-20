from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..models import Application
from ..serializers import ApplicationSerializer, CustomUserSerializer


class ApplicationView(APIView):
    """
    Представление для управления экземплярами Application, связанными с учителем.

    Обрабатывает получение данных о заявке и создание/обновление заявок
    для аутентифицированного пользователя.
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Получить email текущего пользователя, статус администратора и активный статус.

        Возвращает:
            Response: Содержит email пользователя, статус администратора и активный статус.
        """
        user = request.user

        if user.is_superuser:
            applications = Application.objects.all()
            serializer = ApplicationSerializer(applications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        try:
            application = Application.objects.get(teacher_email=user.email)
            serializer = ApplicationSerializer(application)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Application.DoesNotExist:
            return Response({"error": "Заявка не найдена или доступ запрещен."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        """
        Создать новую заявку для текущего пользователя.

        Данные запроса должны включать хотя бы один класс участника.
        В случае успеха возвращаются данные созданной заявки.

        Возвращает:
            Response: Данные заявки, если она успешно создана, иначе ошибки.
        """
        user = request.user
        data = request.data.copy()
        data['teacher_email'] = user.email  # Связываем заявку с email пользователя

        # Проверяем, предоставлен ли хотя бы один класс участника
        if not any("class" in key for key in data.keys()):
            return Response({"message": "Заполните одного из участников"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """
        Обновить существующую заявку для текущего пользователя.

        Если поле не предоставлено в данных запроса и является необязательным,
        оно будет установлено в None.

        Возвращает:
            Response: Данные обновленной заявки, если успешно, иначе ошибки.
        """
        user = request.user
        data = request.data

        for value in data:
            print(value)


        # Проверяем, предоставлен ли хотя бы один класс участника
        if not any("class" in key for key in data.keys()) :
            return Response({"message": "Заполните одного из участников"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            application = Application.objects.get(teacher_email=user.email)
        except Application.DoesNotExist:
            return Response({"error": "Заявка не найдена или доступ запрещен."}, status=status.HTTP_404_NOT_FOUND)

        # Получаем все поля модели Application
        fields = Application._meta.get_fields()
        # Извлекаем названия полей, которые могут быть пустыми
        fields_names = [field.name for field in fields if field.null and field.blank]

        # Обнуляем значения полей, которые не указаны в данных запроса
        for field in fields_names:
            if field not in data or data.get(field) in [None, '', "null"]:
                setattr(application, field, None)  # Заменяем значение на None

        serializer = self.serializer_class(application, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
