from django.db import models
from decimal import Decimal
from clientes.models import Clientes
from rat.models import Rat
from datetime import datetime
# Create your models here.

class Orcamento(models.Model):
    nome_local = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True, blank=True, related_name='orcamentos_local')
    nome_usuarios = models.ForeignKey(Rat, on_delete=models.SET_NULL, null=True, blank=True, related_name='orcamentos_usuario')
   
    data_acionamento = models.DateTimeField(null=True, blank=True)
    data_chegada = models.DateTimeField(null=True, blank=True)
    sla_resposta = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),null=True, blank=True)

    class Meta:
        verbose_name = 'Orçamento'
        verbose_name_plural = 'Orçamentos'
        ordering = ['-data_acionamento']

    def save(self, *args, **kwargs):
        if self.data_chegada and self.data_acionamento:
            # Calcula a diferença em horas
            diff = self.data_chegada - self.data_acionamento
            hours = diff.total_seconds() / 3600
            self.sla_resposta = Decimal(str(hours))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Orçamento {self.nome_usuarios} - {self.nome_local}"

