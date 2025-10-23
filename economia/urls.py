from django.urls import path
from .views import home_view, receitas_view, despesas_view, investimentos_view, contas_view

urlpatterns = [
    path('', home_view, name='home'),
    path('receitas/', receitas_view, name='receitas'),
    path('despesas/', despesas_view, name='despesas'),
    path('investimentos/', investimentos_view, name='investimentos'),
    path('contas/', contas_view, name='contas'),
]