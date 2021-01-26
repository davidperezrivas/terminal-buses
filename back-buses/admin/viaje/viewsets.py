from rest_framework import viewsets
from .models import Viaje
from .serializer import ViajeSerializer

class ViajeViewSet(viewsets.ModelViewSet):

    queryset = Viaje.objects.all()
    serializer_class = ViajeSerializer

