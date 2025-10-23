from django.contrib import admin
from .models import Receita, Despesa, Investimento, ContasPagar
# Register your models here.

@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data')
    search_fields = ('descricao',)
    list_filter = ('data',)
    
@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data')
    search_fields = ('descricao',)
    list_filter = ('data',)
    
@admin.register(Investimento)
class InvestimentoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data')
    search_fields = ('descricao',)
    list_filter = ('data',)
    
@admin.register(ContasPagar)
class ContasPagarAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'vencimento', 'pago')
    search_fields = ('descricao',)
    list_filter = ('pago', 'vencimento')