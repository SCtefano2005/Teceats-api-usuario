from django.db import models
from restaurantes.models import Repartidor
from pedidos.models import Pedido

class Entrega(models.Model):
    fecha_hora_entrega = models.DateTimeField(auto_now_add=True)
    direccion_entrega = models.CharField(max_length=255)
    pedido = models.ForeignKey(
        Pedido, 
        on_delete=models.CASCADE, 
        related_name='entregas'
    )
    repartidor = models.ForeignKey(
        Repartidor, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='entregas'
    )

    def __str__(self):
        return f"Entrega {self.id} - Pedido {self.pedido.id} - Repartidor {self.repartidor}"