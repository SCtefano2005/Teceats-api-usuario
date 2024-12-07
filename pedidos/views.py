from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Pedido, DetallePedido
from .serializers import PedidoSerializer, DetallePedidoSerializer
from django.db.models import Q


class IsOwnerOrRestaurantOwner(permissions.BasePermission):
    """
    Permite el acceso a los dueños del pedido o a los dueños del restaurante relacionado.
    """
    def has_object_permission(self, request, view, obj):
        # Verifica si el usuario autenticado es el dueño del pedido o el dueño del restaurante
        if hasattr(request.user, 'usuario'):
            return obj.usuario == request.user.usuario  # Usuario que hizo el pedido
        elif hasattr(request.user, 'dueñorestaurante'):
            return obj.restaurante.id_dueno == request.user.dueñorestaurante  # Dueño del restaurante
        return False


class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrRestaurantOwner]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'usuario'):
            # Filtra pedidos donde el usuario autenticado es el cliente
            return Pedido.objects.filter(usuario=user.usuario)
        elif hasattr(user, 'dueñorestaurante'):
            # Filtra pedidos relacionados con restaurantes del dueño
            return Pedido.objects.filter(restaurante__id_dueno=user.dueñorestaurante)
        return Pedido.objects.none()

    def perform_create(self, serializer):
        # Asigna el usuario autenticado como el cliente del pedido
        if hasattr(self.request.user, 'usuario'):
            serializer.save(usuario=self.request.user.usuario)
        else:
            raise serializers.ValidationError("Solo los usuarios pueden crear pedidos.")

    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        pedido = self.get_object()
        nuevo_estado = request.data.get('estado')
        if nuevo_estado in dict(Pedido.ESTADOS):
            pedido.estado = nuevo_estado
            pedido.save()
            return Response({'estado': pedido.estado}, status=status.HTTP_200_OK)
        return Response({'error': 'Estado no válido'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def marcar_como_recibido(self, request, pk=None):
        """Marcar el pedido como 'entregado' cuando el cliente recibe el pedido."""
        try:
            pedido = self.get_object()

            # Verificar que el usuario autenticado sea el cliente del pedido
            if not hasattr(request.user, 'usuario') or pedido.usuario != request.user.usuario:
                return Response({"error": "No tienes permisos para cambiar el estado de este pedido."}, status=status.HTTP_403_FORBIDDEN)

            # Verificar que el estado actual sea 'enviado'
            if pedido.estado != 'enviado':
                return Response({"error": "El estado del pedido no es válido para marcar como recibido."}, status=status.HTTP_400_BAD_REQUEST)

            # Cambiar el estado a 'entregado'
            pedido.estado = 'entregado'
            pedido.save()

            return Response({'estado': pedido.estado}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DetallePedidoViewSet(viewsets.ModelViewSet):
    serializer_class = DetallePedidoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrRestaurantOwner]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'usuario'):
            # Filtra detalles relacionados con pedidos del cliente autenticado
            return DetallePedido.objects.filter(pedido__usuario=user.usuario)
        elif hasattr(user, 'dueñorestaurante'):
            # Filtra detalles relacionados con pedidos de restaurantes del dueño
            return DetallePedido.objects.filter(pedido__restaurante__id_dueno=user.dueñorestaurante)
        return DetallePedido.objects.none()

    def perform_create(self, serializer):
        pedido = serializer.validated_data['pedido']
        if hasattr(self.request.user, 'usuario') and pedido.usuario != self.request.user.usuario:
            raise serializers.ValidationError("No tienes permisos para agregar detalles a este pedido.")
        elif hasattr(self.request.user, 'dueñorestaurante') and pedido.restaurante.id_dueno != self.request.user.dueñorestaurante:
            raise serializers.ValidationError("No tienes permisos para agregar detalles a este pedido.")
        serializer.save()
