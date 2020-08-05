from django.db import models


class StockSymbol(models.Model):
    name = models.CharField(max_length=50, blank=True)
    symbol = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class BrokerageService(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class StockTrade(models.Model):
    stock = models.ForeignKey(StockSymbol, on_delete=models.CASCADE)
    time = models.DateTimeField()
    share_price = models.DecimalField(decimal_places=2, max_digits=7+2)
    share_amount = models.DecimalField(decimal_places=6, max_digits=7+6)
    total_amount = models.DecimalField(decimal_places=2, max_digits=7+2)
    trade_type = models.BooleanField(choices=(
        (True, 'Buy'),
        (False, 'Sell')
    ))
    brokerage_service = models.ForeignKey(BrokerageService, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['stock', 'time', 'share_price', 'total_amount'], name='unique trade')
        ]

    def __str__(self):
        trade_type_name = "Buy" if self.trade_type else "Sell"
        return "{} {}".format(trade_type_name, self.stock.symbol)
