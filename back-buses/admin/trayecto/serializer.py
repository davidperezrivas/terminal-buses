from rest_framework import serializers
from .models import Trayecto

class TrayectoSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Trayecto
        fields  = '__all__' 
