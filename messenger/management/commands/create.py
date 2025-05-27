from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """Database Create"""

    def handle(self, *args, **options):
        print('DATABASE CREATE RUN Successfully')

