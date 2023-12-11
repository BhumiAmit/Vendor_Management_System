# historical_performance/urls.py
from django.urls import path
from .views import HistoricalPerformanceListAPIView, HistoricalPerformanceDetailAPIView

urlpatterns = [
    path('api/historical_performance/', HistoricalPerformanceListAPIView.as_view(), name='historical-performance-list'),
    path('api/historical_performance/<int:pk>/', HistoricalPerformanceDetailAPIView.as_view(), name='historical-performance-detail'),
]
