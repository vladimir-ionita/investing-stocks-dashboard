from django.core.management.base import BaseCommand

from .import_stock_trades_utilities.EmailImporter import EmailImporter
from .import_stock_trades_utilities.RobinhoodStockTradeMapper import RobinhoodStockTradeMapper


class Command(BaseCommand):
    help = "Import stock trades from email"

    def add_arguments(self, parser):
        parser.add_argument('email', help="email address to be used for import")
        parser.add_argument('password', help="email password")
        parser.add_argument('search_criteria', help="email search criteria according to RFC3501 section 6.4.4")

    def handle(self, *args, **options):
        username = options['email']
        password = options['password']
        search_criteria = options['search_criteria']
        verbose = int(options['verbosity']) > 0

        email_body_list = EmailImporter(username, password, search_criteria, verbose, self.stdout)\
            .import_emails_body_list()
        share_trades = RobinhoodStockTradeMapper.get_share_trades_from_emails(email_body_list)

        if verbose:
            self.stdout.write(self.style.SUCCESS('Successfully fetched {} stock trades'.format(len(share_trades))))

