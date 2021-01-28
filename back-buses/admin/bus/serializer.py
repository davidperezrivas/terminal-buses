from rest_framework import serializers
from .models import Bus
from chofer.serializer import ChoferSerializer

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Bus
        fields  = '__all__' 

    def to_representation(self, instance):
        self.fields['chofer_asignado'] =  ChoferSerializer(read_only=True)
        return super(BusSerializer, self).to_representation(instance)
