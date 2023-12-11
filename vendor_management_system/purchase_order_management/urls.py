from django.urls import path
from .views import (
    PurchaseOrderListCreateAPIView,
    PurchaseOrderRetrieveUpdateDestroyAPIView,
    AcknowledgePurchaseOrderView
)

urlpatterns = [
    path('api/purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchaseorder-list-create'),
    path('api/purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='purchaseorder-detail'),
    path('api/purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge-purchase-order'),
]
