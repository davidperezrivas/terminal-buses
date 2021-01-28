from rest_framework import viewsets
from .models import Bus
from .serializer import BusSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from datetime import datetime, timedelta, date


class BusViewSet(viewsets.ModelViewSet):

    queryset = Bus.objects.all()
    serializer_class = BusSerializer


