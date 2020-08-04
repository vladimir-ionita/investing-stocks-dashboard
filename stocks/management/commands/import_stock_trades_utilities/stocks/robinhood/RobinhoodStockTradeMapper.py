from datetime import datetime
import pytz

from stocks.management.commands.import_stock_trades_utilities.stocks.StockTradeType import StockTradeType
from stocks.management.commands.import_stock_trades_utilities.stocks.WholeShareStockTrade import WholeShareStockTrade
from stocks.management.commands.import_stock_trades_utilities.stocks.FractionalShareStockTrade import \
    FractionalShareStockTrade


class RobinhoodStockTradeMapper:
    @staticmethod
    def get_stock_trades_from_emails(email_body_list):
        return [x for x in map(RobinhoodStockTradeFactory.make_share_trade_from_email_body, email_body_list)
                if x is not None]


class RobinhoodStockTradeFactory:
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
            trade_type=StockTradeType(trade_description_parts[TRADE_TYPE_INDEX]),
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
            trade_type=StockTradeType(trade_description_parts[TRADE_TYPE_INDEX]),
            share_amount=float(trade_description_parts[TRADE_SHARES_AMOUNT_INDEX]),
            share_price=float(trade_description_parts[TRADE_SHARE_PRICE_INDEX][1:]),
            time=timezone.localize(datetime.strptime(date_time_string, date_time_format))
        )
