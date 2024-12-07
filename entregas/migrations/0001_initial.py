# Generated by Django 4.2.5 on 2024-12-07 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurantes', '0001_initial'),
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_entrega', models.DateTimeField(auto_now_add=True)),
                ('direccion_entrega', models.CharField(max_length=255)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entregas', to='pedidos.pedido')),
                ('repartidor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entregas', to='restaurantes.repartidor')),
            ],
        ),
    ]
