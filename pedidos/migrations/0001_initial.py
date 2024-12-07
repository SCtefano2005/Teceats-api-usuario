# Generated by Django 4.2.5 on 2024-12-07 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurantes', '0001_initial'),
        ('platos', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('En Proceso', 'En Proceso'), ('Entregado', 'Entregado')], default='Pendiente', max_length=20)),
                ('restaurante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to='restaurantes.restaurante')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to='usuarios.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('precio_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='pedidos.pedido')),
                ('plato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles_pedido', to='platos.plato')),
            ],
        ),
    ]
