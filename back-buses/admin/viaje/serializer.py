from rest_framework import serializers
from .models import Viaje
from pasajero.serializer import PasajeroSerializer
from trayecto.serializer import TrayectoSerializer

class ViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Viaje
        fields  = '__all__' 


    def to_representation(self, instance):
        self.fields['trayecto'] =  TrayectoSerializer(read_only=True)
        self.fields['pasajero'] =  PasajeroSerializer(read_only=True)
        return super(ViajeSerializer, self).to_representation(instance)
