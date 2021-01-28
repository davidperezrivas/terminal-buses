from django.db import models
from pasajero.models import Pasajero
from trayecto.models import Trayecto

# Create your models here.
class Viaje(models.Model):
    pasajero        = models.ForeignKey(Pasajero, on_delete=models.SET_NULL, blank=True, null=True)
    trayecto        = models.ForeignKey(Trayecto, on_delete=models.CASCADE)
    create_at       = models.DateTimeField(auto_now=True)
    num_asiento     = models.IntegerField()
    


    class Meta:
        verbose_name_plural = "Viajes"