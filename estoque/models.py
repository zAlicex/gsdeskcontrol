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
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE, null=True, blank=True, related_name='usos_estoque')
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade Usada")

    def __str__(self):
        return f"{self.local} - {self.usuario} - {self.data_hora:%d/%m/%Y %H:%M} - {self.get_status_display()}"

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    quantidade = models.PositiveIntegerField(null=True, blank=True, verbose_name="Quantidade Disponível")

    def __str__(self):
        return self.nome

class Licencas(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='licencas', verbose_name="Produto")
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade de Licenças")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor da Licença")
    data_registro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registro")
    
    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade} licenças - R$ {self.valor}"
    
    def save(self, *args, **kwargs):
        # Subtrai a quantidade de licenças da quantidade disponível do produto
        if self.pk is None:  # Se é um novo registro
            if self.produto.quantidade is not None:
                self.produto.quantidade = max(0, self.produto.quantidade - self.quantidade)
                self.produto.save()
        super().save(*args, **kwargs)