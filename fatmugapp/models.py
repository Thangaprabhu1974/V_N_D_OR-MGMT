from django.db import models
from django.db.models.signals import post_save, post_delete

from .signals import logger
from .utils import (
    calculate_average_response_time,
    calculate_quality_rating_avg,
    calculate_on_time_delivery_rate,
    calculate_fulfillment_rate
)

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=10, unique=True, blank=True)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_metrics()

    def save(self, *args, **kwargs):
        if not self.vendor_code:
            self.vendor_code = self.generate_unique_vendor_code()
        super().save(*args, **kwargs)
        for performance in self.historicalperformance_set.all():
            performance.save()
        self.update_metrics()

    def update_metrics(self):
        try:
            self.on_time_delivery_rate = calculate_on_time_delivery_rate(self)
            logger.debug(f"Updated on-time delivery rate to {self.on_time_delivery_rate} for vendor {self.name}")
        except Exception as e:
            logger.error(f"Failed to update on-time delivery rate for vendor {self.name}: {e}")

        try:
            self.quality_rating_avg = calculate_quality_rating_avg(self)
            logger.debug(f"Updated quality rating average to {self.quality_rating_avg} for vendor {self.name}")
        except Exception as e:
            logger.error(f"Failed to update quality rating average for vendor {self.name}: {e}")

        try:
            self.average_response_time = calculate_average_response_time(self)
            logger.debug(f"Updated average response time to {self.average_response_time} for vendor {self.name}")
        except Exception as e:
            logger.error(f"Failed to update average response time for vendor {self.name}: {e}")

        try:
            self.fulfillment_rate = calculate_fulfillment_rate(self)
            logger.debug(f"Updated fulfillment rate to {self.fulfillment_rate} for vendor {self.name}")
        except Exception as e:
            logger.error(f"Failed to update fulfillment rate for vendor {self.name}: {e}")

    def generate_unique_vendor_code(self):
        import uuid
        return str(uuid.uuid4())[:10]



class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=10, unique=True, blank=True)  # Retained for display purposes
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"Purchase Order {self.id}"  # Use id instead of po_number

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if it's a new instance
            self.generate_po_number()
        super().save(*args, **kwargs)

    def generate_po_number(self):
        import uuid
        self.po_number = str(uuid.uuid4())[:10]


from datetime import datetime

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.vendor} - {self.date}"

    def save(self, *args, **kwargs):
        # Calculate the values from the related Vendor instance
        self.on_time_delivery_rate = self.vendor.on_time_delivery_rate
        self.quality_rating_avg = self.vendor.quality_rating_avg
        self.average_response_time = self.vendor.average_response_time
        self.fulfillment_rate = self.vendor.fulfillment_rate

        # Set the date to the current date and time
        self.date = datetime.now()

        super().save(*args, **kwargs)



class PurchaseOrderDelivery(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    delivery_date = models.DateTimeField()
    status = models.CharField(max_length=100)
    actual_delivery_date = models.DateTimeField(null=True, blank=True)


# models.py

# Existing model definitions

# Signal registration
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=PurchaseOrder)
def update_actual_delivery_date(sender, instance, created, **kwargs):
    from .models import PurchaseOrderDelivery

    if instance.status == 'completed':
        po_delivery, created = PurchaseOrderDelivery.objects.get_or_create(
            po=instance,
            defaults={
                'vendor': instance.vendor,
                'delivery_date': instance.delivery_date,
                'status': instance.status,
                'actual_delivery_date': instance.delivery_date,
            }
        )
        if not created:
            po_delivery.actual_delivery_date = instance.delivery_date
            po_delivery.save()
