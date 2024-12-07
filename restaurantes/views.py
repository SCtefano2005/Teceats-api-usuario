from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Restaurante, Repartidor
from .serializers import RestauranteSerializer, RepartidorSerializer


# Permiso personalizado para validar que el usuario es un dueño de restaurante
class IsOwnerOfRestaurante(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'dueñorestaurante')

    def has_object_permission(self, request, view, obj):
        # Validar que el restaurante pertenezca al dueño autenticado
        return obj.id_dueno == request.user


# ViewSet para Restaurante
class RestauranteViewSet(viewsets.ModelViewSet):
    serializer_class = RestauranteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfRestaurante]

    def get_queryset(self):
        """Filtrar restaurantes por el dueño autenticado."""
        if hasattr(self.request.user, 'dueñorestaurante'):
            return Restaurante.objects.filter(id_dueno=self.request.user)
        return Restaurante.objects.none()

    def perform_create(self, serializer):
        """Asignar el restaurante al dueño autenticado."""
        if not hasattr(self.request.user, 'dueñorestaurante'):
            raise serializers.ValidationError("No tienes permisos para crear un restaurante.")
        serializer.save(id_dueno=self.request.user)

    def perform_update(self, serializer):
        """Asegurar que solo el dueño pueda actualizar el restaurante."""
        if serializer.instance.id_dueno != self.request.user:
            raise serializers.ValidationError("No tienes permiso para modificar este restaurante.")
        serializer.save()

    def perform_destroy(self, instance):
        """Asegurar que solo el dueño pueda eliminar el restaurante."""
        if instance.id_dueno != self.request.user:
            raise serializers.ValidationError("No tienes permiso para eliminar este restaurante.")
        instance.delete()

    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        """Cambiar el estado de un restaurante (Pendiente/Aprobado/Rechazado)."""
        restaurante = self.get_object()
        nuevo_estado = request.data.get('status')
        if nuevo_estado in dict(Restaurante.STATUS_CHOICES):
            restaurante.status = nuevo_estado
            restaurante.save()
            return Response({'status': restaurante.status})
        return Response({'error': 'Estado no válido'}, status=400)


# ViewSet para Repartidor
class RepartidorViewSet(viewsets.ModelViewSet):
    serializer_class = RepartidorSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfRestaurante]

    def get_queryset(self):
        """Filtrar repartidores por los restaurantes del dueño autenticado."""
        if hasattr(self.request.user, 'dueñorestaurante'):
            return Repartidor.objects.filter(restaurante__id_dueno=self.request.user)
        return Repartidor.objects.none()

    def perform_create(self, serializer):
        """Asegurar que solo el dueño pueda agregar repartidores a sus restaurantes."""
        restaurante = serializer.validated_data['restaurante']
        if restaurante.id_dueno != self.request.user:
            raise serializers.ValidationError("No tienes permiso para agregar repartidores a este restaurante.")
        serializer.save()

    def perform_update(self, serializer):
        """Asegurar que solo el dueño pueda actualizar el repartidor."""
        repartidor = serializer.instance
        if repartidor.restaurante.id_dueno != self.request.user:
            raise serializers.ValidationError("No tienes permiso para modificar este repartidor.")
        serializer.save()

    def perform_destroy(self, instance):
        """Asegurar que solo el dueño pueda eliminar el repartidor."""
        if instance.restaurante.id_dueno != self.request.user:
            raise serializers.ValidationError("No tienes permiso para eliminar este repartidor.")
        instance.delete()
