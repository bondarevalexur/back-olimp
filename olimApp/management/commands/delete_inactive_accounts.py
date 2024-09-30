from django.core.management.base import BaseCommand
from django.utils import timezone
from olimApp.models import CustomUser  # Импортируйте вашу модель пользователя
from datetime import timedelta

class Command(BaseCommand):
    help = 'Удаляет неактивированные аккаунты'

    def handle(self, *args, **kwargs):
        # Устанавливаем срок давности для неактивированных аккаунтов
        expiration_date = timezone.now() - timedelta(days=7)  # Например, 7 дней

        # Находим неактивированные аккаунты, созданные до expiration_date
        inactive_users = CustomUser.objects.filter(is_active=False, date_joined__lt=expiration_date)

        # Удаляем неактивированные аккаунты
        count = inactive_users.count()
        inactive_users.delete()

        self.stdout.write(f'Удалено {count} неактивированных аккаунтов.')