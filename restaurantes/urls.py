from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestauranteViewSet, RepartidorViewSet

# Crear el router
router = DefaultRouter()
router.register(r'restaurantes', RestauranteViewSet, basename='restaurante')
router.register(r'repartidores', RepartidorViewSet, basename='repartidor')

urlpatterns = [
    path('', include(router.urls)),  # Incluir todas las rutas generadas por el router
]
