from django.db import models

class SensorLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ph = models.FloatField()
    temperature = models.FloatField()
    water_level_aquarium_cm = models.FloatField()
    water_level_filterbak_cm = models.FloatField()


