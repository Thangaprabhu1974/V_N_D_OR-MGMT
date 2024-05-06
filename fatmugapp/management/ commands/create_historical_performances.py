from datetime import datetime
from .models import Vendor, HistoricalPerformance
from .utils import (
    calculate_on_time_delivery_rate,
    calculate_quality_rating_avg,
    calculate_average_response_time,
    calculate_fulfillment_rate
)


def create_historical_performances_for_all_vendors():
    try:
        vendors = Vendor.objects.all()
        for vendor in vendors:
            # Calculate the metrics for each vendor
            on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
            quality_rating_avg = calculate_quality_rating_avg(vendor)
            average_response_time = calculate_average_response_time(vendor)
            fulfillment_rate = calculate_fulfillment_rate(vendor)

            # Create a new HistoricalPerformance object for the vendor
            performance = HistoricalPerformance(
                vendor=vendor,
                date=datetime.now(),  # Use the current date/time
                on_time_delivery_rate=on_time_delivery_rate,
                quality_rating_avg=quality_rating_avg,
                average_response_time=average_response_time,
                fulfillment_rate=fulfillment_rate
            )
            performance.save()

        return True  # Success
    except Exception as e:
        print(f"Failed to create HistoricalPerformance objects: {e}")
        return False  # Failed


# Call the function to create HistoricalPerformance objects for all vendors
create_historical_performances_for_all_vendors()
