from datetime import datetime

from stocks.management.commands.import_stock_trades_utilities.stocks.StockTradeType import StockTradeType
from stocks.management.commands.import_stock_trades_utilities.DataTypeValidator import DataTypeValidator


class WholeShareStockTrade:
    def __init__(self, stock_symbol, trade_type, share_amount, share_price, time):
        self.stock_symbol = DataTypeValidator.validate_data_type(stock_symbol, str, 'Stock symbol must be a string.')
        self.trade_type = DataTypeValidator.validate_data_type(trade_type,
                                                               StockTradeType,
                                                               'Trade type must be a TradeType.')
        self.share_amount = DataTypeValidator.validate_data_type(share_amount, float, 'Share amount must be a float.')
        self.share_price = DataTypeValidator.validate_data_type(share_price, float, 'Share price must be a float.')
        self.total_amount = self.share_amount * self.share_price
        self.datetime = DataTypeValidator.validate_data_type(time, datetime, 'Time must be a datetime.')

    def __str__(self):
        return f'{self.trade_type.name} {self.stock_symbol} {self.share_amount} {self.share_price} ' \
               f'{self.total_amount} {self.datetime}'
