from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SensorLog  # Zorg ervoor dat je het juiste model importeert
from .serializers import SensorLogSerializer  # Gebruik de juiste serializer naam

class SensorHistoryView(APIView):
    def get(self, request):
        """
        Haal de sensorloggeschiedenis op en retourneer deze.
        Je kunt filters toevoegen op basis van bijvoorbeeld een specifieke datum.
        """
        # Je kunt hier bijvoorbeeld de data filteren op basis van een datum
        # Voorbeeld: SensorLog.objects.filter(timestamp__date='2025-05-01')
        
        # Haal alle loggegevens op (je kunt dit aanpassen naar behoefte)
        sensor_data = SensorLog.objects.all()
        
        # Seriëleer de data
        serializer = SensorLogSerializer(sensor_data, many=True)
        
        # Retourneer de geserialiseerde data als JSON
        return Response(serializer.data)


