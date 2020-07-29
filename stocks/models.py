from django.db import models


class StockSymbol(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)

    def __str__(self):
        return self.name
