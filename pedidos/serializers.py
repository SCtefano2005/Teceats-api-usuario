from rest_framework import serializers
from .models import Pedido, DetallePedido
from platos.models import Plato
from platos.serializers import PlatoSerializer  # Asumiendo que tienes un serializer para Plato
from usuarios.serializers import UsuarioSerializer  # Si necesitas información del usuario
from usuarios.models import Usuario

class DetallePedidoSerializer(serializers.ModelSerializer):
    plato = PlatoSerializer(read_only=True)  # Para mostrar datos del plato
    id_plato = serializers.PrimaryKeyRelatedField(
        queryset=Plato.objects.all(),
        source='plato',
        write_only=True
    )

    class Meta:
        model = DetallePedido
        fields = ['id', 'cantidad', 'precio_total', 'plato', 'id_plato']

class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True, read_only=True)
    usuario = UsuarioSerializer(read_only=True)  # Si necesitas detalles del usuario
    id_usuario = serializers.PrimaryKeyRelatedField(
        source='usuario',
        queryset=Usuario.objects.all(),
        write_only=True
    )

    class Meta:
        model = Pedido
        fields = ['id', 'fecha_hora', 'estado', 'usuario', 'id_usuario', 'restaurante', 'detalles']
