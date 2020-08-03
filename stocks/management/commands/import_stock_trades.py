from django.core.management.base import BaseCommand

from stocks.models import StockSymbol, StockTrade

from .import_stock_trades_utilities.EmailImporter import EmailImporter
from .import_stock_trades_utilities.RobinhoodStockTradeMapper import RobinhoodStockTradeMapper, TradeType


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

        stock_trades_models = []
        for trade in share_trades:
            stock_symbol, _ = StockSymbol.objects.get_or_create(symbol=trade.stock_symbol)
            trade_model = StockTrade(stock=stock_symbol,
                                     time=trade.datetime,
                                     share_price=trade.share_price,
                                     share_amount=trade.share_amount,
                                     total_amount=trade.total_amount,
                                     trade_type=trade.trade_type == TradeType.BUY)
            stock_trades_models.append(trade_model)

        StockTrade.objects.bulk_create(stock_trades_models, ignore_conflicts=True)
        if verbose:
            self.stdout.write(self.style.SUCCESS('Successfully imported {} stock trades'.format(len(share_trades))))
