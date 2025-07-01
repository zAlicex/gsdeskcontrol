from django.db import models
from clientes.models import Clientes
# Create your models here.

class Orpecas(models.Model):
    CHOICES = [
        ('Intrusão', 'Intrusão'),
        ('Ameaça', 'Ameaça'),
        ('Pessoa Suspeita', 'Pessoa Suspeita'),
        
    ]
    local = models.ForeignKey(Clientes, on_delete=models.CASCADE, related_name='OrpecasLocal', default=1)
    diagnostico = models.CharField(max_length=255, choices=CHOICES, null=True, blank=True)
    botao_panico = models.CharField(max_length=255, choices=CHOICES, null=True, blank=True)
    sensor = models.CharField(max_length=255, choices=CHOICES, null=True, blank=True)
    
    def __str__(self):
        return f" {self.local}"
