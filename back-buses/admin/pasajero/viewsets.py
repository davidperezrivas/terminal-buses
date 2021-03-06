from rest_framework import viewsets
from .models import Pasajero
from .serializer import PasajeroSerializer

class PasajeroViewSet(viewsets.ModelViewSet):

    queryset = Pasajero.objects.all()
    serializer_class = PasajeroSerializer

