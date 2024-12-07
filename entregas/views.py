from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Entrega
from .serializers import EntregaSerializer
from django.shortcuts import get_object_or_404
from pedidos.models import Pedido
from restaurantes.models import Repartidor

class IsRepartidorOrAdmin(permissions.BasePermission):
    """
    Permite acceso solo a repartidores o administradores.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Los repartidores solo pueden acceder a sus propias entregas
        if hasattr(request.user, 'repartidor'):
            return obj.repartidor.user == request.user
        # Los administradores tienen acceso total
        return request.user.is_staff

class EntregaViewSet(viewsets.ModelViewSet):
    serializer_class = EntregaSerializer
    permission_classes = [permissions.IsAuthenticated, IsRepartidorOrAdmin]

    def get_queryset(self):
        """Filtra entregas dependiendo de los permisos del usuario."""
        user = self.request.user
        if user.is_staff:
            return Entrega.objects.all()
        # Si es un repartidor, muestra solo sus entregas
        if hasattr(user, 'repartidor'):
            return Entrega.objects.filter(repartidor__user=user)
        # Otros usuarios no tienen acceso
        return Entrega.objects.none()

    def perform_create(self, serializer):
        """Asignar repartidor y pedido a la entrega."""
        user = self.request.user
        if not hasattr(user, 'repartidor'):
            raise PermissionDenied("Solo los repartidores pueden crear entregas.")

        # Verificar que el pedido existe y está asignado al repartidor
        pedido_id = self.request.data.get('pedido_id')
        pedido = get_object_or_404(Pedido, id=pedido_id)

        if pedido.estado != 'enviado':
            raise PermissionDenied("El pedido no está en estado 'enviado'.")

        serializer.save(repartidor=user.repartidor, pedido=pedido)

    def perform_update(self, serializer):
        """Asegura que solo el repartidor asignado pueda actualizar su entrega."""
        entrega = self.get_object()
        if entrega.repartidor.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("No tienes permiso para modificar esta entrega.")
        serializer.save()

    def perform_destroy(self, instance):
        """Permite eliminar entregas solo al administrador."""
        if not self.request.user.is_staff:
            raise PermissionDenied("Solo los administradores pueden eliminar entregas.")
        instance.delete()
