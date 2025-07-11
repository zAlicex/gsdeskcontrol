from django.db import models

class Clientes(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    responsavel = models.CharField(max_length=200, null=True, blank=True, verbose_name="Responsável")
    pronta_resposta = models.CharField(max_length=200, blank=True, null=True, verbose_name="Pronta Resposta")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    
    def __str__(self):
        return str(self.nome) if self.nome else ""

    @property
    def total_produtos(self):
        return sum(rel.quantidade for rel in self.produtos_relacionados.all())

class ClienteProntaResposta(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, related_name='prontas_respostas')
    pronta_resposta = models.CharField(max_length=200, verbose_name="Pronta Resposta")
    ordem = models.PositiveIntegerField(default=0, help_text="Ordem de exibição")
    
    class Meta:
        ordering = ['ordem']
        unique_together = ('cliente', 'pronta_resposta')
    
    def __str__(self):
        return f"{self.cliente.nome} - {self.pronta_resposta}"

class ClienteTelefone(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, related_name='telefones')
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    tipo = models.CharField(max_length=50, blank=True, null=True, verbose_name="Tipo (ex: Celular, Fixo)")
    ordem = models.PositiveIntegerField(default=0, help_text="Ordem de exibição")
    
    class Meta:
        ordering = ['ordem']
        unique_together = ('cliente', 'telefone')
    
    def __str__(self):
        return f"{self.cliente.nome} - {self.telefone}"

class ClienteProduto(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, related_name='produtos_relacionados')
    produto = models.ForeignKey('estoque.Produto', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    class Meta:
        unique_together = ('cliente', 'produto')
    def __str__(self):
        return f"{self.cliente.nome} - {self.produto} ({self.quantidade})"
