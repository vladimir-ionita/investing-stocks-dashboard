from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import stock trades from email"

    def add_arguments(self, parser):
        parser.add_argument('email', help="email address to be used for import")
        parser.add_argument('password', help="email password")
        parser.add_argument('search_criteria', help="email search criteria according to RFC3501 section 6.4.4")

    def handle(self, *args, **options):
        pass
