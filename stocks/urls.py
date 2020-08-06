from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    path('stocks/', views.stocks_page_view, name='stocks')
]
