from .models import Chofer
from rest_framework import serializers


class ChoferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chofer
        fields = '__all__'