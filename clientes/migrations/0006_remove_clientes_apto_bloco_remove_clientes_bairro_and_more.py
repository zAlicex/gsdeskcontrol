# Generated by Django 5.2.3 on 2025-06-27 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0005_alter_clientes_status_servico'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientes',
            name='apto_bloco',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='bairro',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='celular',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='cep',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='cidade',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='cpf_cnpj',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='data_chamado',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='data_instalacao',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='email',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='endereco',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='forma_pagamento',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='numero_os',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='periodo',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='relatorios_servicos_prestados',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='revendedor',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='servicos',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='status_servico',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='tecnicos',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='telefone',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='valor_total',
        ),
    ]
