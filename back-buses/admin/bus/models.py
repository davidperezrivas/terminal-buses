from django.db import models
from chofer.models import Chofer

# Create your models here.
class Bus(models.Model):
    patente             = models.CharField(max_length=10)
    chofer_asignado     = models.ForeignKey(Chofer, on_delete=models.SET_NULL, blank=True, null=True)
    disponible          = models.BooleanField(default=True)
    cantidad_asientos   = models.IntegerField(default=10)
