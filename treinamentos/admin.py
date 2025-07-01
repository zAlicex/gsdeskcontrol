from django.contrib import admin
from .models import Treinamento

@admin.register(Treinamento)
class TreinamentoAdmin(admin.ModelAdmin):
    list_display = ['local', 'usuario', 'data_hora', 'status']
    list_filter = ['status', 'local', 'usuario']
    search_fields = ['local__nome', 'usuario__nome']
    date_hierarchy = 'data_hora'
    ordering = ['-data_hora']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'tipo')
        }),
        ('Local e Instrutor', {
            'fields': ('local', 'instrutor')
        }),
        ('Agendamento', {
            'fields': ('data_inicio', 'data_fim', 'duracao_horas')
        }),
        ('Status e Observações', {
            'fields': ('status', 'observacoes')
        }),
    )
