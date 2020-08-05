import os
import math

from django.core.management.base import BaseCommand
from django.db.models import Sum
from stocks.models import BrokerageService, StockSymbol, StockTrade

import pandas


class Command(BaseCommand):
    help = "Import stock trades from csv"

    def add_arguments(self, parser):
        parser.add_argument('source', help="File source to import from")

    def handle(self, *args, **options):
        file_path = options['source']

        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise FileExistsError('File not found')

        # Read CSV
        df = pandas.read_csv(file_path,
                             parse_dates=['Activity Date', 'Process Date', 'Settle Date'],
                             converters={'Amount': Command.string_to_amount})

        # Remove columns of no interest
        df.drop(columns=['Account Type', 'Suppressed'], inplace=True)

        # Filter trades of interest
        trans_code_of_interest = ['BUY', 'SELL', 'REC']
        is_trade_of_interest = df['Trans Code'].isin(trans_code_of_interest)
        trades = df[is_trade_of_interest]

        # Get stock symbols
        stock_symbols = trades['Instrument'].unique()
        stock_symbols.sort()
        print("Found {} symbols:".format(len(stock_symbols)))
        print(stock_symbols)
        print()

        # Print trades difference for every stock symbol
        brokerage_service = BrokerageService.objects.get(name="Robinhood")
        for symbol in stock_symbols:
            trades_for_symbol = trades[trades['Instrument'] == symbol]
            trades_for_symbol_spent = trades_for_symbol['Amount'].sum()

            symbol_model = StockSymbol.objects.get(symbol=symbol)
            trade_models = StockTrade.objects.filter(stock=symbol_model, brokerage_service=brokerage_service)
            trade_models_spent = trade_models.aggregate(Sum('total_amount'))['total_amount__sum']

            spent_difference = trades_for_symbol_spent - float(trade_models_spent)
            if not math.isclose(trades_for_symbol_spent, trade_models_spent) and spent_difference > 0.2:
                print("{}:\t{} trades for ${:.2f} in DB vs {} trades for ${:.2f} in CSV [{:.4f}]".format(
                    symbol,
                    len(trade_models), trade_models_spent,
                    trades_for_symbol.shape[0], trades_for_symbol_spent,
                    spent_difference)
                )
                print(trades_for_symbol)
                print()

    @staticmethod
    def string_to_amount(description):
        description = description.replace('(', '')
        description = description.replace(')', '')
        description = description.replace('$', '')
        if Command.is_number(description):
            return float(description)
        else:
            return 0.0

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
