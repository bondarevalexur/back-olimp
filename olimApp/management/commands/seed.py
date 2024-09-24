from django.core.management.base import BaseCommand
from olimApp.models import Page

class Command(BaseCommand):
    help = 'Create seed data for Page model'
    pages = ["Главная"]

    def handle(self, *args, **kwargs):
        Page.objects.create(title="Главная", content="Главная", slug="main")
        Page.objects.create(title="Методические материалы", content="Методические", slug="methods")
        Page.objects.create(title="Контакты", content="Контакты", slug="contacts")
        Page.objects.create(title="Педагогам", content="Педагогам", slug="teaches")
        Page.objects.create(title="Участникам", content="Участникам", slug="participant")
        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))