from django.db import models

# Create your models here.
class Chofer(models.Model):
    nombre      = models.CharField(max_length=50)
    apellido    = models.CharField(max_length=50)
    run         = models.CharField(max_length=10, unique=True )
    direccion   = models.CharField(max_length=50)
    telefono    = models.CharField(max_length=50)
    email       = models.CharField(max_length=50)
    disponible  = models.BooleanField(default=True)


    def __str__(self):
        return f'{self.nombre} - { self.apellido } - {self.run} - {self.email} - {self.disponible} '

    class Meta:
        verbose_name_plural = "Choferes"
