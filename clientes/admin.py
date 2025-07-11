from django.contrib import admin
from .models import Clientes, ClienteProduto, ClienteProntaResposta, ClienteTelefone

class ClienteProntaRespostaInline(admin.TabularInline):
    model = ClienteProntaResposta
    extra = 1
    fields = ['pronta_resposta', 'ordem']

class ClienteTelefoneInline(admin.TabularInline):
    model = ClienteTelefone
    extra = 1
    fields = ['telefone', 'tipo', 'ordem']

class ClienteProdutoInline(admin.TabularInline):
    model = ClienteProduto
    extra = 1

@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ['nome', 'pronta_resposta', 'telefone', 'total_produtos']
    search_fields = ['nome', 'pronta_resposta', 'telefone']
    inlines = [ClienteProntaRespostaInline, ClienteTelefoneInline, ClienteProdutoInline]

@admin.register(ClienteProduto)
class ClienteProdutoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'produto', 'quantidade']
    list_filter = ['produto']
    search_fields = ['cliente__nome', 'produto__nome']

@admin.register(ClienteProntaResposta)
class ClienteProntaRespostaAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'pronta_resposta', 'ordem']
    list_filter = ['cliente']
    search_fields = ['cliente__nome', 'pronta_resposta']
    ordering = ['cliente', 'ordem']

@admin.register(ClienteTelefone)
class ClienteTelefoneAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'telefone', 'tipo', 'ordem']
    list_filter = ['cliente', 'tipo']
    search_fields = ['cliente__nome', 'telefone']
    ordering = ['cliente', 'ordem']
