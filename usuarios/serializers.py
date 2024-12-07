from rest_framework import serializers
from .models import Usuario, DueñoRestaurante

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre', 'correo_electronico', 'telefono', 'google_id']  # Incluir el campo telefono


class DueñoRestauranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DueñoRestaurante
        fields = ['nombre', 'correo_electronico', 'telefono', 'google_id']