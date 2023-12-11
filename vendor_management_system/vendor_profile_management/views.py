from django.db import models
from rest_framework import generics
from django.db.models import Avg, ExpressionWrapper, F, Count
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from .models import Vendor
from .serializers import VendorSerializer

class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Vendor Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class VendorPerformanceView(generics.RetrieveAPIView):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()  

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        total_pos = instance.purchaseorder_set.count()
        completed_pos = instance.purchaseorder_set.filter(status='completed')
        successfully_fulfilled_pos = completed_pos.exclude(issue_date__isnull=False)


        # Calculate performance metrics
        # on_time_delivery_rate = instance.on_time_delivery_rate
        # quality_rating_avg = instance.quality_rating_avg
        # average_response_time = instance.average_response_time
        # fulfillment_rate = instance.fulfillment_rate

        # # You can customize the response format as needed
        # performance_data = {
        #     "on_time_delivery_rate": on_time_delivery_rate,
        #     "quality_rating_avg": quality_rating_avg,
        #     "average_response_time": average_response_time,
        #     "fulfillment_rate": fulfillment_rate,
        # }

        # return Response(performance_data)
        # Calculate performance metrics
        completed_pos = instance.purchaseorder_set.filter(status='completed')  # Adjust the status filtering as needed
        total_completed_pos = completed_pos.count()

        # Calculate On-Time Delivery Rate
        on_time_delivered_pos = completed_pos.filter(delivery_date__lte=timezone.now())
        on_time_delivery_count = on_time_delivered_pos.count()

        on_time_delivery_rate = (
            on_time_delivery_count / total_completed_pos
        ) if total_completed_pos > 0 else 0.0

        # Other performance metrics
        quality_rating_avg = completed_pos.filter(quality_rating__isnull=False).aggregate(Avg('quality_rating'))['quality_rating__avg']
        
        # Calculate Average Response Time
        response_times = completed_pos.filter(
            acknowledgment_date__isnull=False,
            issue_date__isnull=False
        ).annotate(
            response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=models.DurationField())
        ).aggregate(avg_response_time=Avg('response_time'))

        average_response_time = response_times['avg_response_time'] if response_times['avg_response_time'] else 0.0

        # Calculate Fulfilment Rate
        fulfillment_rate = (
            successfully_fulfilled_pos.count() / total_pos
        ) if total_pos > 0 else 0.0

        # You can customize the response format as needed
        performance_data = {
            "on_time_delivery_rate": on_time_delivery_rate,
            "quality_rating_avg": quality_rating_avg,
            "average_response_time": average_response_time,
            "fulfilment_rate": fulfillment_rate,
        }

        return Response(performance_data)

