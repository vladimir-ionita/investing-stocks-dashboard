from django.shortcuts import render, redirect, reverse

from . import models


def home_page_view(request):
    return redirect(reverse('stocks:stocks'), permanent=True)


def stocks_page_view(request):
    stock_symbol_list = models.StockSymbol.objects.all()
    context_stocks = []
    for stock_symbol in stock_symbol_list:
        stock_description = {
            'stock': stock_symbol.symbol,
            'shares': stock_symbol.shares_owned,
            'current_investments': stock_symbol.current_investments,
            'cheapest_share': stock_symbol.cheapest_share_price,
            'most_expensive_share': stock_symbol.most_expensive_share_price
        }
        context_stocks.append(stock_description)

    context = {
        'stocks_description_fields': [
            'Stock',
            'Shares',
            'Current Investments',
            'Cheapest share price',
            'Most expensive share'
        ],
        'stocks_description': context_stocks,
    }

    return render(request, "stocks/stocks.html", context)
