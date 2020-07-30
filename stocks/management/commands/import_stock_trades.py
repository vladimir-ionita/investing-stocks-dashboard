from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import stock trades from email"

    def handle(self, *args, **options):
        pass
