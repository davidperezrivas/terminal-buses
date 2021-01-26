from rest_framework import viewsets

from .models import Chofer
from .serializer import ChoferSerializer

class ChoferViewSet(viewsets.ModelViewSet):
    queryset = Chofer.objects.all()
    serializer_class = ChoferSerializer