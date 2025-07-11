from django.urls import path
from . import views

app_name = 'locais'

urlpatterns = [
    # A URL principal agora aponta para a nova view unificada
    path('', views.clientes_view, name='locais'), 
    
    # URL da API para buscar os dados de um cliente
    path('get_cliente/<int:cliente_id>/', views.get_cliente, name='get_cliente'),
    
    # URL para carregar mais clientes via AJAX
    path('carregar-mais/', views.carregar_mais_clientes, name='carregar_mais_clientes'),
    
    # URL para salvar um novo cliente
    path('salvar/', views.salvar_cliente, name='salvar_cliente'),

    # API de locais
    path('locais-api/', views.locais_api, name='locais_api'),
    
    # Endpoint JSON com todas as informações dos clientes
    path('locais_json/', views.locais_json, name='locais_json'),

    # URL para carregar a lista de clientes via AJAX (partial)
    path('lista_clientes_partial/', views.lista_clientes_partial, name='lista_clientes_partial'),
    
    # URL para adicionar pronta resposta e telefone juntos
    path('cliente/<int:cliente_id>/adicionar-pronta-telefone/', views.adicionar_pronta_telefone, name='adicionar_pronta_telefone'),
    
    # URLs para adicionar/remover pronta resposta individualmente
    path('cliente/<int:cliente_id>/adicionar-pronta-resposta/', views.adicionar_pronta_resposta, name='adicionar_pronta_resposta'),
    path('cliente/<int:cliente_id>/remover-pronta-resposta/<int:pronta_resposta_id>/', views.remover_pronta_resposta, name='remover_pronta_resposta'),
    
    # URLs para adicionar/remover telefone individualmente
    path('cliente/<int:cliente_id>/adicionar-telefone/', views.adicionar_telefone, name='adicionar_telefone'),
    path('cliente/<int:cliente_id>/remover-telefone/<int:telefone_id>/', views.remover_telefone, name='remover_telefone'),
]