from django.db import models

# Create your models here.

class Clientes(models.Model):
    nome = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
