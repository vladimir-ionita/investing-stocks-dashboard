from enum import Enum
from datetime import datetime


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

        return FractionalShareTrade(trade_description_parts[TRADE_STOCK_INDEX],
                                    TradeType(trade_description_parts[TRADE_TYPE_INDEX]),
                                    trade_description_parts[TRADE_SHARES_AMOUNT_INDEX],
                                    trade_description_parts[TRADE_SHARE_PRICE_INDEX],
                                    trade_description_parts[TRADE_PRICE_AMOUNT_INDEX],
                                    datetime.strptime(date_time_string, date_time_format))

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

        return WholeShareTrade(trade_description_parts[TRADE_STOCK_INDEX],
                               TradeType(trade_description_parts[TRADE_TYPE_INDEX]),
                               trade_description_parts[TRADE_SHARES_AMOUNT_INDEX],
                               trade_description_parts[TRADE_SHARE_PRICE_INDEX],
                               datetime.strptime(date_time_string, date_time_format))


class TradeType(Enum):
    BUY = 'buy'
    SELL = 'sell'


class WholeShareTrade:
    def __init__(self, stock_symbol, trade_type, share_amount, share_price, time):
        self.stock_symbol = stock_symbol
        self.trade_type = trade_type
        self.share_amount = share_amount
        self.share_price = share_price
        self.datetime = time

    def __str__(self):
        return ' '.join([self.trade_type.name,
                         self.stock_symbol,
                         self.share_amount,
                         self.share_price,
                         str(self.datetime)])


class FractionalShareTrade:
    def __init__(self, stock_symbol, trade_type, share_amount, share_price, total_amount, time):
        self.stock_symbol = stock_symbol
        self.trade_type = trade_type
        self.share_amount = share_amount
        self.share_price = share_price
        self.total_amount = total_amount
        self.datetime = time

    def __str__(self):
        return ' '.join([self.trade_type.name,
                         self.stock_symbol,
                         self.share_amount,
                         self.share_price,
                         self.total_amount,
                         str(self.datetime)])
