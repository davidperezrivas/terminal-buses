from django.db import models
from bus.models import Bus

# Create your models here.
class Trayecto(models.Model):
    origen          = models.CharField(max_length=70)
    destino         = models.CharField(max_length=70)
    precio          = models.IntegerField()
    fecha_salida    = models.DateTimeField()
    fecha_llegada   = models.DateTimeField()
    bus_asignado    = models.ForeignKey(Bus, on_delete=models.SET_NULL, blank=True, null=True)
    disponible      = models.BooleanField(default=True)



    def __str__(self):
        return f'{self.origen} - { self.destino } - {self.precio} - {self.fecha_salida} - {self.fecha_llegada} '

    class Meta:
        verbose_name_plural = "Trayectos"