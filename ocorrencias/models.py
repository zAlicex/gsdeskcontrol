from django.db import models
from clientes.models import Clientes

class Ocorrencia(models.Model):
    STATUS_CHOICES = [
        ('portas_abertas', 'Portas e Portões Abertos'),
        ('inibicao_cameras', 'Inibição de Câmeras e Sensores'),
        ('botao_panico', 'Acionamento indevido de Botão de Pânico'),
    ]

    local = models.ForeignKey(Clientes, on_delete=models.CASCADE, null=True, blank=True)
    data_hora = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='portas_abertas')
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.local} - {self.data_hora:%d/%m/%Y %H:%M} - {self.get_status_display()}"
