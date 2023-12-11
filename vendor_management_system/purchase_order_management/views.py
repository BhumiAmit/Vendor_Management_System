from django.db.models import F, ExpressionWrapper, fields, Avg
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import PurchaseOrder, Vendor
from .serializers import PurchaseOrderSerializer, AcknowledgePurchaseOrderSerializer

class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Purchase Order Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
    
# class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
#     queryset = PurchaseOrder.objects.all()
#     serializer_class = PurchaseOrderSerializer

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()

#         # Update acknowledgment_date
#         serializer = AcknowledgePurchaseOrderSerializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         # Trigger recalculation of average_response_time for the vendor
#         instance.vendor.average_response_time

#         return Response({"message": "Purchase Order acknowledged successfully","data": serializer.data,}, status=status.HTTP_200_OK)
class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Update acknowledgment_date
        serializer = AcknowledgePurchaseOrderSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Trigger recalculation of average_response_time for the vendor
        response_time_expression = ExpressionWrapper(
            F('acknowledgment_date') - F('issue_date'),
            output_field=fields.DurationField(),
        )
        average_response_time = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            acknowledgment_date__isnull=False,
            issue_date__isnull=False
        ).aggregate(average_response_time=Avg(response_time_expression))['average_response_time']

        # Convert timedelta to seconds
        average_response_time = average_response_time.total_seconds() if average_response_time else 0.0

        # Update Vendor model with the average response time
        Vendor.objects.filter(id=instance.vendor.id).update(
            average_response_time=average_response_time
        )

        return Response({
            "message": "Purchase Order acknowledged successfully",
            "data": serializer.data,
        }, status=status.HTTP_200_OK)