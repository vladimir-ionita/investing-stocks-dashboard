from django.core.management.base import BaseCommand

from stocks.models import BrokerageService, StockSymbol, StockTrade

from .import_stock_trades_utilities.email.EmailImporter import EmailImporter
from .import_stock_trades_utilities.stocks.robinhood.RobinhoodStockTradeMapper import RobinhoodStockTradeMapper
from .import_stock_trades_utilities.stocks.StockTradeType import StockTradeType

BROKERAGE_SERVICE_ROBINHOOD = "Robinhood"


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

        email_body_list = EmailImporter(
            username,
            password,
            search_criteria,
            verbose,
            self.stdout
        ).import_emails_body_list()
        stock_trade_objects = RobinhoodStockTradeMapper.get_stock_trades_from_emails(email_body_list)

        if verbose:
            self.stdout.write(self.style.SUCCESS(
                'Successfully fetched {} stock trades'.format(len(stock_trade_objects)))
            )

        stock_trades_models = []
        brokerage_service, _ = BrokerageService.objects.get_or_create(name=BROKERAGE_SERVICE_ROBINHOOD)
        for trade in stock_trade_objects:
            stock_symbol, _ = StockSymbol.objects.get_or_create(symbol=trade.stock_symbol)
            trade_model = StockTrade(stock=stock_symbol,
                                     time=trade.datetime,
                                     share_price=trade.share_price,
                                     share_amount=trade.share_amount,
                                     total_amount=trade.total_amount,
                                     trade_type=trade.trade_type == StockTradeType.BUY,
                                     brokerage_service=brokerage_service)
            stock_trades_models.append(trade_model)

        stm_amount = StockTrade.objects.bulk_create(stock_trades_models, ignore_conflicts=True)
        if verbose:
            self.stdout.write(self.style.SUCCESS(
                'Successfully imported {} stock trades'.format(len(stm_amount)))
            )
