# Generated by Django 5.1.2 on 2025-07-03 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0009_remove_clientes_quantidade_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='quantidade',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
