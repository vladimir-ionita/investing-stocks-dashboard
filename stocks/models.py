from django.db import models


class StockSymbol(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)

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
