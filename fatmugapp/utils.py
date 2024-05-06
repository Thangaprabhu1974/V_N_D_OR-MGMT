import logging

logger = logging.getLogger(__name__)

def calculate_fulfillment_rate(vendor_id):
    from .models import PurchaseOrder

    total_orders_count = PurchaseOrder.objects.filter(vendor=vendor_id).count()
    successful_orders_count = PurchaseOrder.objects.filter(
        vendor=vendor_id, status='completed'
    ).count()

    logger.debug(f"Total orders for vendor {vendor_id}: {total_orders_count}")
    logger.debug(f"Successful orders for vendor {vendor_id}: {successful_orders_count}")

    if total_orders_count > 0:
        fulfillment_rate = (successful_orders_count / total_orders_count) * 100
        logger.info(f"Calculated fulfillment rate for vendor {vendor_id}: {fulfillment_rate:.2f}%")
    else:
        fulfillment_rate = None
        logger.info(f"No completed orders for vendor {vendor_id}")

    logger.debug(f"Fulfillment rate for vendor {vendor_id}: {fulfillment_rate}")

    return fulfillment_rate

from django.db.models import Avg
from datetime import timedelta

import logging
from django.db.models import Avg, F

import logging
from django.db.models import Avg, F


logger = logging.getLogger(__name__)

def calculate_average_response_time(vendor_id):
    from .models import PurchaseOrder
    logger.debug(f"Calculating average response time for vendor {vendor_id}")

    acknowledged_orders = PurchaseOrder.objects.filter(vendor=vendor_id, acknowledgment_date__isnull=False)

    if acknowledged_orders.exists():
        response_times = acknowledged_orders.annotate(response_time=F('acknowledgment_date') - F('issue_date'))
        avg_response_time = response_times.aggregate(avg_response_time=Avg('response_time'))['avg_response_time']
        if avg_response_time:
            total_hours = avg_response_time.total_seconds() / 3600
            avg_response_time_days = total_hours / 24
            logger.debug(f"Average response time calculated for vendor {vendor_id}: {avg_response_time_days:.2f} days")
            return avg_response_time_days
    logger.debug(f"No acknowledged orders found for vendor {vendor_id}")
    return None





def calculate_quality_rating_avg(vendor_id):
    from .models import PurchaseOrder
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor_id, status='completed', quality_rating__isnull=False)

    if completed_orders.exists():
        avg_quality_rating = completed_orders.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating']
    else:
        avg_quality_rating = None

    return avg_quality_rating


import logging


logger = logging.getLogger(__name__)


def calculate_on_time_delivery_rate(vendor_id):
    from .models import PurchaseOrder
    from .models import PurchaseOrderDelivery
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor_id, status='completed')
    completed_count = completed_orders.count()

    logger.debug(f"Total completed orders for vendor {vendor_id}: {completed_count}")

    if completed_count > 0:
        on_time_delivery_count = 0
        for po in completed_orders:
            # Retrieve the corresponding PurchaseOrderDelivery instance
            try:
                po_delivery = PurchaseOrderDelivery.objects.get(po=po)
            except PurchaseOrderDelivery.DoesNotExist:
                logger.warning(f"No delivery information found for PO {po.po_number}")
                continue

            # Compare the expected delivery date with the actual delivery date
            if po_delivery.actual_delivery_date and po.delivery_date <= po_delivery.actual_delivery_date:
                on_time_delivery_count += 1

        logger.debug(f"Total on-time delivery orders for vendor {vendor_id}: {on_time_delivery_count}")

        on_time_delivery_rate = (on_time_delivery_count / completed_count) * 100
        logger.info(f"Calculated on-time delivery rate for vendor {vendor_id}: {on_time_delivery_rate:.2f}%")
    else:
        logger.info(f"No completed orders for vendor {vendor_id}")
        on_time_delivery_rate = None

    logger.debug(f"On-time delivery rate for vendor {vendor_id}: {on_time_delivery_rate}")

    return on_time_delivery_rate


# utils.py
def calculate_historical_metrics(vendor):
    on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
    quality_rating_avg = calculate_quality_rating_avg(vendor)
    average_response_time = calculate_average_response_time(vendor)
    fulfillment_rate = calculate_fulfillment_rate(vendor)

    return on_time_delivery_rate, quality_rating_avg, average_response_time, fulfillment_rate
