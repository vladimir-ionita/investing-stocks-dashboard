from django.shortcuts import render


def stocks_page_view(request):
    return render(request, "stocks/stocks.html", {})
