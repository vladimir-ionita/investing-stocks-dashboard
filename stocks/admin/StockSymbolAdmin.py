from django.contrib import admin

from stocks.models import StockSymbol


@admin.register(StockSymbol)
class StockSymbolAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name')
    fieldsets = ()

    search_fields = ('symbol', 'name')
    ordering = ('symbol',)
    filter_horizontal = ()
