from rest_framework import viewsets
from .models import Bus
from .serializer import BusSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from datetime import datetime, timedelta, date

# Create your views here.

class BusViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows Capacitación Historico to be viewed.
    """
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

    #filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['periodo', 'grado_especializacion', 'criticidad', 'objetivo_estrategico', 'tipo_curso', 'ceco']

