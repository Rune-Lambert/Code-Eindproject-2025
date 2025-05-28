# LiveData/urls.py
from django.urls import path
from .views import SensorHistoryView

urlpatterns = [
    path('sensor-history/', SensorHistoryView.as_view(), name='sensor-history'),
]
