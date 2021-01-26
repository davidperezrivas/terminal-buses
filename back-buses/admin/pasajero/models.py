from django.db import models

# Create your models here.
class Pasajero(models.Model):
    nombre          = models.CharField(max_length=50)
    apellido        = models.CharField(max_length=50)
    run             = models.CharField(max_length=10)
    telefono        = models.CharField(max_length=15)
    email           = models.EmailField(max_length=50)

    def __str__(self):
        return str(self.nombre) + ' ' + str(self.apellido) + ' ' + str(self.run)

    class Meta:
        verbose_name_plural = "Pasajeros"



