from django.db import models

# Create your models here.
class Chofer(models.Model):
    nombre      = models.CharField(max_length=50)
    apellido    = models.CharField(max_length=50)
    run         = models.CharField(max_length=10)
    direccion   = models.CharField(max_length=50)
    telefono    = models.CharField(max_length=50)
    email       = models.CharField(max_length=50)
    disponible  = models.BooleanField(default=True)