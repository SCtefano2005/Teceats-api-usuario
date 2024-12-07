from django.db import models
from restaurantes.models import Restaurante
from usuarios.models import Usuario
from platos.models import Plato

class Pedido(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Entregado', 'Entregado'),
    ]

    fecha_hora = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos')
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='pedidos')

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario} - {self.estado}"
    
class DetallePedido(models.Model):
    cantidad = models.PositiveIntegerField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, related_name='detalles_pedido')

    def __str__(self):
        return f"Detalle Pedido {self.id} - {self.plato.nombre} - Cantidad: {self.cantidad}"