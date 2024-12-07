from django.urls import path
from . import views

urlpatterns = [
    path("usuarios/login/", views.google_login_usuario, name="google_login_usuario"),
    path("usuarios/callback/", views.google_callback_usuario, name="google_callback_usuario"),
    path("duenos/login/", views.google_login_dueno, name="google_login_dueno"),
    path("duenos/callback/", views.google_callback_dueno, name="google_callback_dueno"),
]
