from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('stocks/', views.stocks_page_view, name='stocks')
]
