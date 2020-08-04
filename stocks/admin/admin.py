from django.contrib import admin

from stocks import models

admin.site.register(models.StockSymbol)
admin.site.register(models.BrokerageService)
