from django.db import models
from django.utils import timezone
from clientes.models import Clientes
from rat.models import Rat

class Estoque(models.Model):
    STATUS_CHOICES = [
        ('realizado', 'Realizado'),
        ('programado', 'Programado'),
        ('pendente', 'Pendente'),
    ]

    local = models.ForeignKey(Clientes, on_delete=models.CASCADE, related_name='registros_agenda',null=True, blank=True)
    usuario = models.ForeignKey(Rat, on_delete=models.CASCADE, related_name='registros_agenda',null=True, blank=True)
    data_hora = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f"{self.local} - {self.usuario} - {self.data_hora:%d/%m/%Y %H:%M} - {self.get_status_display()}"

class Produto(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome