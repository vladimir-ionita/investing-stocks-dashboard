from django.contrib import admin

from stocks import models

admin.site.register(models.StockSymbol)
admin.site.register(models.BrokerageService)


class TradeTypeListFilter(admin.SimpleListFilter):
    title = 'trade type'
    parameter_name = 'trade_type'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            (True, 'Buy'),
            (False, 'Sell'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(trade_type=self.value())
        return queryset.all()


@admin.register(models.StockTrade)
class StockTradeAdmin(admin.ModelAdmin):
    list_display = ('stock', 'share_price', 'share_amount', 'total_amount', 'trade_type', 'time',)
    list_filter = ('stock__symbol', TradeTypeListFilter)
    fieldsets = ()

    search_fields = ('stock',)
    ordering = ('time',)
    filter_horizontal = ()

    def get_readonly_fields(self, request, obj=None):
        if obj:     # edit mode
            return 'stock', 'share_price', 'share_amount', 'total_amount', 'trade_type', 'time',
        else:       # create mode
            return []
