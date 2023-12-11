from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from vendor_profile_management.models import Vendor
from historical_performance.models import HistoricalPerformance
from django.db.models import Count, Avg, F, ExpressionWrapper, fields

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=255, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=255, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO-{self.po_number}"

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    vendor = instance.vendor

    # On-Time Delivery Rate
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_delivery_rate = completed_orders.filter(delivery_date__lte=F('acknowledgment_date')).count() / completed_orders.count() * 100 if completed_orders.count() > 0 else 0.0

    # Quality Rating Average
    quality_rating_avg = completed_orders.filter(quality_rating__isnull=False).aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0.0

    # Average Response Time
    response_times = completed_orders.exclude(acknowledgment_date__isnull=True).annotate(
    response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=fields.DurationField())
    )
    average_response_time = response_times.aggregate(average_response_time=Avg('response_time'))['average_response_time'] or 0.0

    # Convert timedelta to seconds
    average_response_time = average_response_time.total_seconds() if average_response_time else 0.0


    # Fulfilment Rate
    fulfillment_rate = completed_orders.filter(status='completed').count() / PurchaseOrder.objects.filter(vendor=vendor).count() * 100 if PurchaseOrder.objects.filter(vendor=vendor).count() > 0 else 0.0

    # Update Vendor metrics
    Vendor.objects.filter(id=vendor.id).update(
        on_time_delivery_rate=on_time_delivery_rate,
        quality_rating_avg=quality_rating_avg,
        average_response_time=average_response_time,
        fulfillment_rate=fulfillment_rate
    )

    # Update Historical Performance
    HistoricalPerformance.objects.create(
        vendor=vendor,
        on_time_delivery_rate=on_time_delivery_rate,
        quality_rating_avg=quality_rating_avg,
        average_response_time=average_response_time,
        fulfillment_rate=fulfillment_rate
    )
