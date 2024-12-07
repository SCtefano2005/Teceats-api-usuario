from django.db import models


class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    correo_electronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    google_id = models.CharField(max_length=255, unique=True)
    token_acceso = models.CharField(max_length=255, blank=True, null=True)
    token_refresh = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre

class DueñoRestaurante(models.Model):
    nombre = models.CharField(max_length=255)
    correo_electronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    google_id = models.CharField(max_length=255, unique=True)
    token_acceso = models.CharField(max_length=255, blank=True, null=True)
    token_refresh = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre