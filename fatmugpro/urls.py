from django.contrib import admin
from django.urls import path

from fatmugapp.views import VendorViewSet, home, PurchaseOrderViewSet, vendor_performance, acknowledge_purchase_order

urlpatterns = [
    path('', home, name='home'),  # Home page view at the root URL
    path('admin/', admin.site.urls),  # Django admin route
    path('api/vendors/', VendorViewSet.as_view({'get': 'list', 'post': 'create'}), name='vendor-list'),  # List and create endpoint for vendors
    path('api/vendors/<int:pk>/', VendorViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='vendor-detail'),  # Detail, update, partial update, and delete endpoint for vendors
     path('api/purchase_orders/', PurchaseOrderViewSet.as_view({'post': 'create', 'get': 'list'}), name='purchase-order-list'),  # Create and list purchase orders
    path('api/purchase_orders/<int:pk>/', PurchaseOrderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='purchase-order-detail'),  # Retrieve, update, and delete purchase orders
    path('api/vendors/<int:vendor_id>/performance/', vendor_performance, name='vendor_performance'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', acknowledge_purchase_order, name='acknowledge-purchase-order'),
    # Acknowledge purchase order endpoint
]