from django.urls import path
from . import views

urlpatterns = [
    # Crear un plato
    path('restaurantes/<int:restaurante_id>/platos/', views.create_plato, name='create_plato'),
    
    # Ver un plato
    path('restaurantes/<int:restaurante_id>/platos/<int:plato_id>/', views.detail_plato, name='detail_plato'),
    
    # Actualizar un plato
    path('restaurantes/<int:restaurante_id>/platos/<int:plato_id>/update/', views.update_plato, name='update_plato'),
    
    # Eliminar un plato
    path('restaurantes/<int:restaurante_id>/platos/<int:plato_id>/delete/', views.delete_plato, name='delete_plato'),
]
