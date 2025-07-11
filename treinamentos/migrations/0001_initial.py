# Generated by Django 5.2.3 on 2025-06-30 10:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0006_remove_clientes_apto_bloco_remove_clientes_bairro_and_more'),
        ('rat', '0005_alter_rat_options_remove_rat_cliente_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Treinamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200, verbose_name='Título do Treinamento')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('tipo', models.CharField(choices=[('tecnico', 'Técnico'), ('operacional', 'Operacional'), ('seguranca', 'Segurança'), ('administrativo', 'Administrativo')], default='tecnico', max_length=20, verbose_name='Tipo')),
                ('data_inicio', models.DateTimeField(verbose_name='Data de Início')),
                ('data_fim', models.DateTimeField(verbose_name='Data de Fim')),
                ('duracao_horas', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Duração (horas)')),
                ('status', models.CharField(choices=[('agendado', 'Agendado'), ('em_andamento', 'Em Andamento'), ('concluido', 'Concluído'), ('cancelado', 'Cancelado')], default='agendado', max_length=20)),
                ('observacoes', models.TextField(blank=True, verbose_name='Observações')),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('instrutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='treinamentos_instrutor', to='rat.rat')),
                ('local', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='treinamentos', to='clientes.clientes')),
                ('participantes', models.ManyToManyField(blank=True, related_name='treinamentos_participante', to='rat.rat')),
            ],
            options={
                'verbose_name': 'Treinamento',
                'verbose_name_plural': 'Treinamentos',
                'ordering': ['-data_inicio'],
            },
        ),
    ]
