from django.urls import path
from . import views

app_name = 'treinamentos'

urlpatterns = [
    path('', views.treinamentos, name='treinamentos'),
    path('get/<int:treinamento_id>/', views.get_treinamento, name='get_treinamento'),
    path('atualizar/<int:treinamento_id>/', views.atualizar_treinamento, name='atualizar_treinamento'),
] 