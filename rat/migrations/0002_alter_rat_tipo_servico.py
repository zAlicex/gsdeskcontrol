# Generated by Django 5.2.3 on 2025-06-21 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rat',
            name='tipo_servico',
            field=models.CharField(blank=True, choices=[('garantia', 'Garantia'), ('corretiva', 'Corretiva'), ('Instalação', 'Instalação')], max_length=20, null=True, verbose_name='Tipo de Serviço'),
        ),
    ]
