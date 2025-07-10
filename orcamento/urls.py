from django.urls import path
from . import views

app_name = 'orcamento'

urlpatterns = [
    path('', views.lista_orcamentos, name='lista_orcamentos'),
    path('novo/', views.novo_orcamento, name='novo_orcamento'),
    path('<int:pk>/editar/', views.editar_orcamento, name='editar_orcamento'),
    path('<int:pk>/dados/', views.get_orcamento_data, name='get_orcamento_data'),
    
    # Endpoint JSON para acionamentos
    path('acionamentos_json/', views.acionamentos_json, name='acionamentos_json'),
] 