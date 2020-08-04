from enum import Enum
from datetime import datetime
import pytz


class RobinhoodStockTradeMapper:
    @staticmethod
    def get_share_trades_from_emails(email_body_list):
        return [x for x in map(RobinhoodShareTradeFactory.make_share_trade_from_email_body, email_body_list)
                if x is not None]


class RobinhoodShareTradeFactory:
    @classmethod
    def make_share_trade_from_email_body(cls, email_body):
        body_parts = email_body.split('\n')
        for line in body_parts:
            if line.startswith("Your market order") \
                    and "was partially executed" not in line \
                    and "was canceled on" not in line:
                return cls.make_share_trade_from_trade_description(line)
        return None

    @classmethod
    def make_share_trade_from_trade_description(cls, trade_description):
        trade_description_parts = trade_description.split(' ')
        if cls.__check_if_whole_share_trade(trade_description_parts):
            return cls.__make_whole_share_trade(trade_description_parts)
        else:
            return cls.__make_fractional_share_trade(trade_description_parts)

    @classmethod
    def __check_if_whole_share_trade(cls, trade_description_parts):
        WHOLE_SHARE_TRADE_MARKER_WORD = 'share'
        WHOLE_SHARE_TRADE_MARKER_INDEX = 6
        return trade_description_parts[WHOLE_SHARE_TRADE_MARKER_INDEX].\
            startswith(WHOLE_SHARE_TRADE_MARKER_WORD)

    @classmethod
    def __make_fractional_share_trade(cls, trade_description_parts):
        TRADE_TYPE_INDEX = 4
        TRADE_PRICE_AMOUNT_INDEX = 5
        TRADE_STOCK_INDEX = 7
        TRADE_DATETIME_MONTH_INDEX = 11
        TRADE_DATETIME_DATE_INDEX = 12
        TRADE_DATETIME_YEAR_INDEX = 13
        TRADE_DATETIME_TIME_INDEX = 15
        TRADE_DATETIME_PERIOD_INDEX = 16
        TRADE_SHARES_AMOUNT_INDEX = 21
        TRADE_SHARE_PRICE_INDEX = 28

        date_time_string = ' '.join([
            trade_description_parts[TRADE_DATETIME_MONTH_INDEX],
            trade_description_parts[TRADE_DATETIME_DATE_INDEX][:-3],
            trade_description_parts[TRADE_DATETIME_YEAR_INDEX],
            trade_description_parts[TRADE_DATETIME_TIME_INDEX],
            trade_description_parts[TRADE_DATETIME_PERIOD_INDEX].rstrip()[:-1],
        ])
        date_time_format = '%B %d %Y %I:%M %p'
        timezone = pytz.timezone("EST")

        return FractionalShareStockTrade(
            stock_symbol=trade_description_parts[TRADE_STOCK_INDEX],
            trade_type=TradeType(trade_description_parts[TRADE_TYPE_INDEX]),
            share_amount=float(trade_description_parts[TRADE_SHARES_AMOUNT_INDEX]),
            share_price=float(trade_description_parts[TRADE_SHARE_PRICE_INDEX][1:]),
            total_amount=float(trade_description_parts[TRADE_PRICE_AMOUNT_INDEX][1:]),
            time=timezone.localize(datetime.strptime(date_time_string, date_time_format))
        )

    @classmethod
    def __make_whole_share_trade(cls, trade_description_parts):
        TRADE_TYPE_INDEX = 4
        TRADE_SHARES_AMOUNT_INDEX = 5
        TRADE_STOCK_INDEX = 8
        TRADE_SHARE_PRICE_INDEX = 16
        TRADE_DATETIME_MONTH_INDEX = 18
        TRADE_DATETIME_DATE_INDEX = 19
        TRADE_DATETIME_YEAR_INDEX = 20
        TRADE_DATETIME_TIME_INDEX = 22
        TRADE_DATETIME_PERIOD_INDEX = 23

        date_time_string = ' '.join([
            trade_description_parts[TRADE_DATETIME_MONTH_INDEX],
            trade_description_parts[TRADE_DATETIME_DATE_INDEX][:-3],
            trade_description_parts[TRADE_DATETIME_YEAR_INDEX],
            trade_description_parts[TRADE_DATETIME_TIME_INDEX],
            trade_description_parts[TRADE_DATETIME_PERIOD_INDEX].rstrip()[:-1],
        ])
        date_time_format = '%B %d %Y %I:%M %p'
        timezone = pytz.timezone("EST")

        return WholeShareStockTrade(
            stock_symbol=trade_description_parts[TRADE_STOCK_INDEX],
            trade_type=TradeType(trade_description_parts[TRADE_TYPE_INDEX]),
            share_amount=float(trade_description_parts[TRADE_SHARES_AMOUNT_INDEX]),
            share_price=float(trade_description_parts[TRADE_SHARE_PRICE_INDEX][1:]),
            time=timezone.localize(datetime.strptime(date_time_string, date_time_format))
        )


class TradeType(Enum):
    BUY = 'buy'
    SELL = 'sell'


class WholeShareStockTrade:
    def __init__(self, stock_symbol, trade_type, share_amount, share_price, time):
        self.stock_symbol = DataTypeValidator.validate_data_type(stock_symbol, str, 'Stock symbol must be a string.')
        self.trade_type = DataTypeValidator.validate_data_type(trade_type, TradeType, 'Trade type must be a TradeType.')
        self.share_amount = DataTypeValidator.validate_data_type(share_amount, float, 'Share amount must be a float.')
        self.share_price = DataTypeValidator.validate_data_type(share_price, float, 'Share price must be a float.')
        self.total_amount = self.share_amount * self.share_price
        self.datetime = DataTypeValidator.validate_data_type(time, datetime, 'Time must be a datetime.')

    def __str__(self):
        return f'{self.trade_type.name} {self.stock_symbol} {self.share_amount} {self.share_price} ' \
               f'{self.total_amount} {self.datetime}'


class FractionalShareStockTrade:
    def __init__(self, stock_symbol, trade_type, share_amount, share_price, total_amount, time):
        self.stock_symbol = DataTypeValidator.validate_data_type(stock_symbol, str, 'Stock symbol must be a string.')
        self.trade_type = DataTypeValidator.validate_data_type(trade_type, TradeType, 'Trade type must be a TradeType.')
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


class DataTypeValidator:
    @staticmethod
    def validate_data_type(variable, data_type, exception_error_message):
        if isinstance(variable, data_type):
            return variable
        else:
            raise ValueError(exception_error_message)
