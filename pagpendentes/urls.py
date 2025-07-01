from django.urls import path
from .views import pagpendentes_view, get_pagpendente

app_name = 'pagpendentes'

urlpatterns = [
    path('', pagpendentes_view, name='pagpendentes'),
    path('get/<int:pendente_id>/', get_pagpendente, name='get_pagpendente'),
] 