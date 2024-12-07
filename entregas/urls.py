from django.urls import path
from . import views

urlpatterns = [
    # Crear una entrega
    path('entregas/', views.EntregaViewSet.as_view({'post': 'create'}), name='crear_entrega'),
    
    # Listar todas las entregas
    path('entregas/', views.EntregaViewSet.as_view({'get': 'list'}), name='listar_entregas'),
    
    # Detalle, actualizar y eliminar una entrega específica
    path('entregas/<int:pk>/', views.EntregaViewSet.as_view({
        'get': 'retrieve', 
        'put': 'update', 
        'delete': 'destroy'
    }), name='detalle_actualizar_eliminar_entrega'),
]
