from rest_framework import serializers
from .models import Trayecto
from bus.serializer import BusSerializer


class TrayectoSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Trayecto
        fields  = '__all__' 

    def to_representation(self, instance):
        self.fields['bus_asignado'] =  BusSerializer(read_only=True)
        return super(TrayectoSerializer, self).to_representation(instance)