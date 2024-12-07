from rest_framework import serializers
from .models import Plato
import cloudinary.uploader

class PlatoSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(write_only=True, required=False)  # Campo para subir la imagen como archivo
    imagen_url = serializers.CharField(read_only=True)  # Solo lectura para devolver la URL de Cloudinary

    class Meta:
        model = Plato
        fields = ['id', 'nombre', 'descripcion', 'precio', 'id_restaurante', 'imagen', 'imagen_url']

    def create(self, validated_data):
        imagen = validated_data.pop('imagen', None)
        
        # Subir la imagen a Cloudinary si se proporciona
        if imagen:
            cloudinary_response = cloudinary.uploader.upload(imagen)
            validated_data['imagen_url'] = cloudinary_response.get('url')
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        imagen = validated_data.pop('imagen', None)
        
        # Subir la nueva imagen a Cloudinary si se proporciona
        if imagen:
            cloudinary_response = cloudinary.uploader.upload(imagen)
            validated_data['imagen_url'] = cloudinary_response.get('url')

        return super().update(instance, validated_data)
