from django.shortcuts import get_object_or_404
from .serializers import PlatoSerializer
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Plato
from restaurantes.models import Restaurante
from usuarios.models import DueñoRestaurante

# Crear un plato
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_plato(request, restaurante_id):
    """Crear un nuevo plato en el restaurante del dueño autenticado."""
    try:
        # Obtener el restaurante
        restaurante = get_object_or_404(Restaurante, id=restaurante_id)
        
        # Verificar si el usuario autenticado es el dueño del restaurante
        dueño_restaurante = DueñoRestaurante.objects.filter(user=request.user).first()
        if not dueño_restaurante or restaurante.id_dueno != dueño_restaurante.id:
            return Response({"error": "No tienes permisos para crear platos en este restaurante."}, status=status.HTTP_403_FORBIDDEN)

        # Crear el plato
        serializer = PlatoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(id_restaurante=restaurante)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Ver un plato
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def detail_plato(request, restaurante_id, plato_id):
    """Obtener los detalles de un plato del restaurante del dueño autenticado."""
    try:
        # Obtener el restaurante
        restaurante = get_object_or_404(Restaurante, id=restaurante_id)
        
        # Verificar si el usuario autenticado es el dueño del restaurante
        dueño_restaurante = DueñoRestaurante.objects.filter(user=request.user).first()
        if not dueño_restaurante or restaurante.id_dueno != dueño_restaurante.id:
            return Response({"error": "No tienes permisos para ver este plato."}, status=status.HTTP_403_FORBIDDEN)

        # Obtener el plato
        plato = get_object_or_404(Plato, id=plato_id, id_restaurante=restaurante)
        serializer = PlatoSerializer(plato)
        return Response(serializer.data)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Actualizar un plato
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_plato(request, restaurante_id, plato_id):
    """Actualizar un plato en el restaurante del dueño autenticado."""
    try:
        # Obtener el restaurante
        restaurante = get_object_or_404(Restaurante, id=restaurante_id)
        
        # Verificar si el usuario autenticado es el dueño del restaurante
        dueño_restaurante = DueñoRestaurante.objects.filter(user=request.user).first()
        if not dueño_restaurante or restaurante.id_dueno != dueño_restaurante.id:
            return Response({"error": "No tienes permisos para modificar este plato."}, status=status.HTTP_403_FORBIDDEN)

        # Obtener el plato
        plato = get_object_or_404(Plato, id=plato_id, id_restaurante=restaurante)
        serializer = PlatoSerializer(plato, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Eliminar un plato
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_plato(request, restaurante_id, plato_id):
    """Eliminar un plato del restaurante del dueño autenticado."""
    try:
        # Obtener el restaurante
        restaurante = get_object_or_404(Restaurante, id=restaurante_id)
        
        # Verificar si el usuario autenticado es el dueño del restaurante
        dueño_restaurante = DueñoRestaurante.objects.filter(user=request.user).first()
        if not dueño_restaurante or restaurante.id_dueno != dueño_restaurante.id:
            return Response({"error": "No tienes permisos para eliminar este plato."}, status=status.HTTP_403_FORBIDDEN)

        # Obtener el plato
        plato = get_object_or_404(Plato, id=plato_id, id_restaurante=restaurante)
        plato.delete()
        return Response({"message": "Plato eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
