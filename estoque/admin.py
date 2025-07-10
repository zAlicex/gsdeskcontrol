from django.contrib import admin
from .models import Produto, Licencas

# Register your models here.
admin.site.register(Produto)

@admin.register(Licencas)
class LicencasAdmin(admin.ModelAdmin):
    list_display = ['produto', 'quantidade', 'valor', 'data_registro']
    list_filter = ['produto', 'data_registro']
    search_fields = ['produto__nome']
    readonly_fields = ['data_registro']
    
    fieldsets = (
        ('Informações da Licença', {
            'fields': ('produto', 'quantidade', 'valor')
        }),
        ('Data de Registro', {
            'fields': ('data_registro',),
            'classes': ('collapse',)
        }),
    )
