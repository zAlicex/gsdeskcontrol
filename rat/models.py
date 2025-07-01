from django.db import models
from clientes.models import Clientes

class Rat(models.Model):
   

    local = models.ForeignKey(Clientes, on_delete=models.CASCADE, related_name='Local', default=1)
    nome = models.CharField(max_length=50, unique=True, verbose_name="Usuario",null=True, blank=True)
    cpf = models.CharField(max_length=20,null=True, blank=True)
    
    

    def __str__(self):
        return f"- {self.nome} - {self.cpf}"

    class Meta:
        verbose_name = "RAT"
        verbose_name_plural = "RATs"
