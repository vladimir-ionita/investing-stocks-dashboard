from django.shortcuts import render, redirect, reverse


def home_page_view(request):
    return redirect(reverse('stocks:stocks'), permanent=True)


def stocks_page_view(request):
    return render(request, "stocks/stocks.html", {})
