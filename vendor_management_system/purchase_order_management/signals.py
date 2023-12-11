from django.db.models.signals import post_save
from django.dispatch import receiver
from purchase_order_management.models import PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    instance.vendor.save()
