import os
import pytz
from datetime import datetime

from django.core.management.base import BaseCommand
from stocks.models import BrokerageService, StockSymbol, StockTrade

from .import_stock_trades_utilities.stocks.StockTradeType import StockTradeType
from .import_stock_trades_local_utilities.FileUtilities import get_sanitized_content_from_file


class Command(BaseCommand):
    help = "Import stock trades from file"

    def add_arguments(self, parser):
        parser.add_argument('source', help="File source to import from")

    def handle(self, *args, **options):
        file_path = options['source']
        verbose = int(options['verbosity']) > 0

        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise FileExistsError('File not found')

        file_content = get_sanitized_content_from_file(file_path)
        stock_trade_models = []
        for line in file_content:
            trade_description_parts = line.split('|')
            date_time_format = '%m/%d/%Y %H:%M:%S'
            timezone = pytz.timezone(trade_description_parts[5][-7:])

            stock_symbol, _ = StockSymbol.objects.get_or_create(symbol=trade_description_parts[0])
            brokerage_service, _ = BrokerageService.objects.get_or_create(name=trade_description_parts[6])
            trade_model = StockTrade(
                stock=stock_symbol,
                time=timezone.localize(datetime.strptime(trade_description_parts[5][:-8], date_time_format)),
                share_price=float(trade_description_parts[3][1:]),
                share_amount=float(trade_description_parts[2]),
                total_amount=float(trade_description_parts[4][1:]),
                trade_type=StockTradeType(trade_description_parts[1].lower()) == StockTradeType.BUY,
                brokerage_service=brokerage_service
            )
            stock_trade_models.append(trade_model)

        StockTrade.objects.bulk_create(stock_trade_models, ignore_conflicts=True)
        if verbose:
            self.stdout.write(self.style.SUCCESS(
                'Successfully imported {} stock trades'.format(len(stock_trade_models)))
            )
