from django.contrib import admin
from .models import Vendor

class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')
    list_filter = ('on_time_delivery_rate', 'quality_rating_avg')
    search_fields = ('name', 'vendor_code')

admin.site.register(Vendor, VendorAdmin)
from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import PurchaseOrder

class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'vendor', 'order_date', 'delivery_date', 'status')
    search_fields = ('po_number', 'vendor__name')
    list_filter = ('status',)

admin.site.register(PurchaseOrder, PurchaseOrderAdmin)

from django.contrib import admin
from .models import Vendor, HistoricalPerformance


# Unregister the existing registration for Vendor
admin.site.unregister(Vendor)

# Register Vendor and HistoricalPerformance models
admin.site.register(Vendor)
admin.site.register(HistoricalPerformance)


from django.contrib import admin
from .models import PurchaseOrderDelivery

@admin.register(PurchaseOrderDelivery)
class PurchaseOrderDeliveryAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'po', 'delivery_date', 'status', 'actual_delivery_date')
    list_filter = ('status', 'delivery_date')
    search_fields = ('vendor__name', 'po__po_number')
    date_hierarchy = 'delivery_date'
