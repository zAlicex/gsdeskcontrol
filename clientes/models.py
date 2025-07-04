from django.db import models

class Clientes(models.Model):
    nome = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return str(self.nome) if self.nome else ""

    @property
    def total_produtos(self):
        return sum(rel.quantidade for rel in self.produtos_relacionados.all())

class ClienteProduto(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, related_name='produtos_relacionados')
    produto = models.ForeignKey('estoque.Produto', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    class Meta:
        unique_together = ('cliente', 'produto')
    def __str__(self):
        return f"{self.cliente.nome} - {self.produto} ({self.quantidade})"
