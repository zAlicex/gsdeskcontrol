from django.urls import path
from .views import OcorrenciasView, get_ocorrencia, atualizar_ocorrencia, excluir_ocorrencia

app_name = 'ocorrencias'

urlpatterns = [
    path('', OcorrenciasView.as_view(), name='ocorrencias'),
    path('get/<int:ocorrencia_id>/', get_ocorrencia, name='get_ocorrencia'),
    path('atualizar/<int:ocorrencia_id>/', atualizar_ocorrencia, name='atualizar_ocorrencia'),
    path('excluir/<int:ocorrencia_id>/', excluir_ocorrencia, name='excluir_ocorrencia'),
] 