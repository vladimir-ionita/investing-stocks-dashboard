from django.db import models
from django.db.models import Sum, Min

import decimal


class StockSymbol(models.Model):
    name = models.CharField(max_length=50, blank=True)
    symbol = models.CharField(max_length=5)

    def __str__(self):
        return self.name

    @property
    def shares_owned(self):
        stock_trade_list = self.stock_trades

        buy_trades = stock_trade_list.filter(trade_type=True)
        bought_shares = buy_trades.aggregate(sum=Sum('share_amount'))['sum'] \
            if buy_trades.count() > 0 \
            else decimal.Decimal(0.0)

        sell_trades = stock_trade_list.filter(trade_type=False)
        sold_shares = sell_trades.aggregate(sum=Sum('share_amount'))['sum'] \
            if sell_trades.count() > 0 \
            else decimal.Decimal(0.0)

        return bought_shares - sold_shares

    @property
    def investments_made(self):
        return self.stock_trades.filter(trade_type=True).aggregate(sum=Sum('total_amount'))['sum']
    
    @property
    def cheapest_share_price(self):
        return self.stock_trades.filter(trade_type=True).aggregate(min=Min('share_price'))['min']


class BrokerageService(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class StockTrade(models.Model):
    stock = models.ForeignKey(StockSymbol, on_delete=models.CASCADE, related_name='stock_trades')
    time = models.DateTimeField()
    share_price = models.DecimalField(decimal_places=2, max_digits=7+2)
    share_amount = models.DecimalField(decimal_places=6, max_digits=7+6)
    total_amount = models.DecimalField(decimal_places=2, max_digits=7+2)
    trade_type = models.BooleanField(choices=(
        (True, 'Buy'),
        (False, 'Sell')
    ))
    brokerage_service = models.ForeignKey(BrokerageService, on_delete=models.CASCADE, related_name='stock_trades')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['stock', 'time', 'share_price', 'total_amount'], name='unique trade')
        ]

    def __str__(self):
        trade_type_name = "Buy" if self.trade_type else "Sell"
        return "{} {}".format(trade_type_name, self.stock.symbol)
