from django.db import models
from clientes.models import Clientes

class PagPendente(models.Model):
    STATUS_CHOICES = [
        ('realizado', 'Realizado'),
        ('programado', 'Programado'),
        ('pendente', 'Pendente'),
    ]

    local = models.ForeignKey(Clientes, on_delete=models.CASCADE, related_name='pagamentos_pendentes')
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f"{self.local} - {self.data_hora:%d/%m/%Y %H:%M} - {self.get_status_display()}"
