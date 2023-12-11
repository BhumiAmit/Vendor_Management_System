# historical_performance/views.py
from rest_framework import generics
from .models import HistoricalPerformance
from .serializers import HistoricalPerformanceSerializer

class HistoricalPerformanceListAPIView(generics.ListCreateAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer

class HistoricalPerformanceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
