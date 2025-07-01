from django.urls import path
from . import views

app_name = 'rondas'

urlpatterns = [
    path('', views.rondas, name='rondas'),
    path('get/<int:ronda_id>/', views.get_ronda, name='get_ronda'),
    path('atualizar/<int:ronda_id>/', views.atualizar_ronda, name='atualizar_ronda'),
] 