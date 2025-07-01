from django.contrib import admin
from .models import Ocorrencia

@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ['local', 'data_hora', 'status', 'observacoes']
    list_filter = ['status', 'local']
    search_fields = ['local__nome', 'observacoes']
    date_hierarchy = 'data_hora'
    ordering = ['-data_hora']
