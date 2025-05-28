# LiveData/serializers.py

from rest_framework import serializers
from .models import SensorLog  # Zorg ervoor dat je het juiste model importeert

class SensorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorLog  # Gebruik het juiste model
        fields = ['timestamp', 'ph', 'temperature', 'water_level_aquarium_cm', 'water_level_filterbak_cm']


