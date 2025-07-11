# Generated by Django 5.1.2 on 2025-06-15 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('endereco', models.CharField(blank=True, max_length=255, null=True)),
                ('bairro', models.CharField(blank=True, max_length=100, null=True)),
                ('cidade', models.CharField(blank=True, max_length=100, null=True)),
                ('cep', models.CharField(blank=True, max_length=10, null=True)),
                ('telefone', models.CharField(blank=True, max_length=20, null=True)),
                ('celular', models.CharField(blank=True, max_length=20, null=True)),
                ('cpf_cnpj', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('numero_os', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('data_chamado', models.DateField(blank=True, null=True)),
                ('revendedor', models.CharField(blank=True, max_length=200, null=True)),
                ('valor_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('forma_pagamento', models.CharField(blank=True, max_length=50, null=True)),
                ('tecnicos', models.CharField(blank=True, max_length=255, null=True)),
                ('periodo', models.CharField(blank=True, max_length=100, null=True)),
                ('data_instalacao', models.DateField(blank=True, null=True)),
                ('status_servico', models.CharField(blank=True, max_length=50, null=True)),
                ('relatorios_servicos_prestados', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
