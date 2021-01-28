from rest_framework import viewsets
from .models import Trayecto
from .serializer import TrayectoSerializer

class TrayectoViewSet(viewsets.ModelViewSet):

    queryset = Trayecto.objects.all()
    serializer_class = TrayectoSerializer

