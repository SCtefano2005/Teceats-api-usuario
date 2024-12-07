from rest_framework import serializers
from .models import Entrega
from pedidos.models import Pedido
from restaurantes.models import Repartidor

class EntregaSerializer(serializers.ModelSerializer):
    # Define los campos que deseas mostrar o recibir
    class Meta:
        model = Entrega
        fields = ['id', 'fecha_hora_entrega', 'direccion_entrega', 'pedido', 'repartidor']
    
    def validate_pedido(self, value):
        """Verifica que el pedido exista antes de ser asignado a la entrega"""
        if not Pedido.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("El pedido no existe.")
        return value

    def validate_repartidor(self, value):
        """Verifica que el repartidor exista antes de ser asignado a la entrega"""
        if value and not Repartidor.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("El repartidor no existe.")
        return value
