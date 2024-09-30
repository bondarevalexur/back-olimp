from django.db import models
from olimApp.models import File


class Page(models.Model):
    """
    Модель для хранения страниц.

    Поля:
        title: Заголовок страницы.
        content: Содержимое страницы.
        slug: Уникальный идентификатор для страницы.
        files: Связь с файлами (многие-ко-многим).
    """

    title = models.CharField(max_length=100, null=True, blank=True)  # Заголовок страницы
    content = models.TextField()  # Содержимое страницы
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)  # Уникальный идентификатор
    files = models.ManyToManyField(
        File, related_name="pages", blank=True
    )  # Связь многие-ко-многим с моделью File

    def __str__(self):
        """
        Возвращает заголовок страницы как строковое представление объекта.

        Возвращает:
            str: Заголовок страницы.
        """
        return self.title