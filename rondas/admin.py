from django.contrib import admin
from .models import Ronda

@admin.register(Ronda)
class RondaAdmin(admin.ModelAdmin):
    list_display = ['local', 'data_hora', 'status', 'observacoes']
    list_filter = ['status', 'local']
    search_fields = ['local__nome', 'observacoes']
    date_hierarchy = 'data_hora'
    ordering = ['-data_hora']
