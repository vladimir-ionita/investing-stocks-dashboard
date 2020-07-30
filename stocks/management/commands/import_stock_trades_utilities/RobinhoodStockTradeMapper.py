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
