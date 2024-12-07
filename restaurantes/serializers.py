from rest_framework import serializers
from .models import Restaurante, Repartidor
from usuarios.models import DueñoRestaurante

class RestauranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurante
        fields = ['id', 'nombre', 'direccion', 'telefono', 'tipo_cocina', 'calificacion', 'delivery_dentro', 'imagen_url', 'status']

    def validate_calificacion(self, value):
        """Validar que la calificación esté entre 0.0 y 5.0."""
        if value is not None and (value < 0 or value > 5):
            raise serializers.ValidationError("La calificación debe estar entre 0.0 y 5.0.")
        return value


class RepartidorSerializer(serializers.ModelSerializer):
    restaurante = serializers.PrimaryKeyRelatedField(queryset=Restaurante.objects.all())

    class Meta:
        model = Repartidor
        fields = ['id', 'nombre', 'telefono', 'vehiculo', 'restaurante']

    def validate_restaurante(self, value):
        """Validar que el restaurante pertenezca al dueño autenticado."""
        user = self.context['request'].user
        try:
            dueño = user.dueñorestaurante  # Acceso al perfil de dueño relacionado con el usuario autenticado
        except DueñoRestaurante.DoesNotExist:
            raise serializers.ValidationError("No tienes un perfil de dueño asociado.")

        if value.id_dueno != dueño:
            raise serializers.ValidationError("No tienes permiso para agregar repartidores a este restaurante.")
        return value
