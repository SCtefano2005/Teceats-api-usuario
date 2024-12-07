from django.urls import path
from .views import PedidoViewSet, DetallePedidoViewSet

urlpatterns = [
    # Rutas para las vistas de pedidos
    path('pedidos/', PedidoViewSet.as_view({'get': 'list', 'post': 'create'}), name='pedido-list'),
    path('pedidos/<int:pk>/', PedidoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='pedido-detail'),
    path('pedidos/<int:pk>/cambiar-estado/', PedidoViewSet.as_view({'post': 'cambiar_estado'}), name='pedido-cambiar-estado'),
    path('pedidos/<int:pk>/marcar-como-recibido/', PedidoViewSet.as_view({'post': 'marcar_como_recibido'}), name='pedido-marcar-como-recibido'),
    
    # Rutas para las vistas de detalles de pedidos
    path('pedidos/<int:pedido_id>/detalles/', DetallePedidoViewSet.as_view({'get': 'list', 'post': 'create'}), name='detallepedido-list'),
    path('pedidos/<int:pedido_id>/detalles/<int:pk>/', DetallePedidoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='detallepedido-detail'),
]
