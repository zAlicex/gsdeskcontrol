from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    path('', views.estoque, name='estoque'),
    path('item/<int:item_id>/', views.get_item_details, name='get_item_details'),
    path('item/edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('item/delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('get/<int:estoque_id>/', views.get_estoque, name='get_estoque'),
    path('atualizar/<int:estoque_id>/', views.atualizar_estoque, name='atualizar_estoque'),
    path('produtos/', views.produto_list, name='produto_list'),
    path('produtos/novo/', views.produto_create, name='produto_create'),
    path('licencas/', views.licencas_list, name='licencas_list'),
    path('licencas/novo/', views.licencas_create, name='licencas_create'),
    path('licencas/resumo/', views.licencas_resumo, name='licencas_resumo'),
    
    # Endpoints JSON
    path('conjunt_json/', views.conjunt_json, name='conjunt_json'),
    path('produtos_json/', views.produtos_json, name='produtos_json'),
    path('licencas_json/', views.licencas_json, name='licencas_json'),
    path('all_models_json/', views.all_models_json, name='all_models_json'),
    
    # Endpoints JSON separados por módulo
    path('clientes_json/', views.clientes_json, name='clientes_json'),
    path('orcamentos_json/', views.orcamentos_json, name='orcamentos_json'),
    path('orpecas_json/', views.orpecas_json, name='orpecas_json'),
    path('ocorrencias_json/', views.ocorrencias_json, name='ocorrencias_json'),
    path('rat_json/', views.rat_json, name='rat_json'),
    path('agenda_json/', views.agenda_json, name='agenda_json'),
    path('pagpendentes_json/', views.pagpendentes_json, name='pagpendentes_json'),
    path('treinamentos_json/', views.treinamentos_json, name='treinamentos_json'),
    path('rondas_json/', views.rondas_json, name='rondas_json'),
]
 
