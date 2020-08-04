from datetime import datetime

from stocks.management.commands.import_stock_trades_utilities.DataTypeValidator import DataTypeValidator
from stocks.management.commands.import_stock_trades_utilities.stocks.StockTradeType import StockTradeType


class FractionalShareStockTrade:
    def __init__(self, stock_symbol, trade_type, share_amount, share_price, total_amount, time):
        self.stock_symbol = DataTypeValidator.validate_data_type(stock_symbol, str, 'Stock symbol must be a string.')
        self.trade_type = DataTypeValidator.validate_data_type(trade_type,
                                                               StockTradeType,
                                                               'Trade type must be a TradeType.')
        self.share_amount = DataTypeValidator.validate_data_type(share_amount, float, 'Share amount must be a float.')
        self.share_price = DataTypeValidator.validate_data_type(share_price, float, 'Share price must be a float.')
        self.total_amount = DataTypeValidator.validate_data_type(total_amount, float, 'Total amount must be float.')
        self.datetime = DataTypeValidator.validate_data_type(time, datetime, 'Time must be a datetime.')

    def __str__(self):
        return '{} {} {} {} {} {}'.format(
            self.trade_type.name,
            self.stock_symbol,
            self.share_amount,
            self.share_price,
            self.total_amount,
            self.datetime
        )
