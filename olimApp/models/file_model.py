import os
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class File(models.Model):
    """
    Модель для хранения файлов.

    Поля:
        name: Имя файла.
        file: Поле для загрузки файла.
        uploaded_at: Дата и время загрузки файла.
    """

    name = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField(
        upload_to="uploads/", null=True, blank=True
    )  # Путь для хранения загруженных файлов
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Дата и время загрузки

    def __str__(self):
        """
        Возвращает имя файла как строковое представление объекта.

        Возвращает:
            str: Имя файла.
        """
        return self.file.name


@receiver(post_delete, sender=File)
def delete_file_from_filesystem(sender, instance, **kwargs):
    """
    Сигнал для удаления файла из файловой системы при удалении записи из базы данных.

    Аргументы:
        sender: Модель, отправившая сигнал.
        instance: Удаляемый экземпляр модели.
        **kwargs: Дополнительные аргументы.
    """
    if instance.file:  # Проверяем, есть ли файл
        if os.path.isfile(instance.file.path):  # Проверяем, существует ли файл
            os.remove(instance.file.path)  # Удаляем файл с файловой системы