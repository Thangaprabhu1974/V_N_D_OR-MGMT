import datetime

from rest_framework import viewsets
from .models import Vendor, HistoricalPerformance
from .serializers import VendorSerializer
from .utils import (
    calculate_on_time_delivery_rate,
    calculate_quality_rating_avg,
    calculate_average_response_time,
    calculate_fulfillment_rate
)

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def perform_create(self, serializer):
        # Call the original perform_create method to save the new Vendor
        instance = serializer.save()

        # Calculate performance metrics for the newly created vendor
        instance.on_time_delivery_rate = calculate_on_time_delivery_rate(instance)
        instance.quality_rating_avg = calculate_quality_rating_avg(instance)
        instance.average_response_time = calculate_average_response_time(instance)
        instance.fulfillment_rate = calculate_fulfillment_rate(instance)

        # Save the updated vendor object
        instance.save()

# Create your views here.


from django.http import HttpResponse, JsonResponse


def home(request):
    return HttpResponse("Welcome to the Fatmug Home Page!")


from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

from datetime import datetime

from datetime import datetime
from django.http import JsonResponse
from .models import Vendor, HistoricalPerformance
from .utils import (
    calculate_on_time_delivery_rate,
    calculate_quality_rating_avg,
    calculate_average_response_time,
    calculate_fulfillment_rate
)

def vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)

        # Calculate performance metrics
        on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
        quality_rating_avg = calculate_quality_rating_avg(vendor)
        average_response_time = calculate_average_response_time(vendor)
        fulfillment_rate = calculate_fulfillment_rate(vendor)

        # Create HistoricalPerformance object and save it
        performance = HistoricalPerformance(
            vendor=vendor,
            date=datetime.now(),  # Use the current date/time
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=quality_rating_avg,
            average_response_time=average_response_time,
            fulfillment_rate=fulfillment_rate
        )
        performance.save()

        # Return the performance data with the generated id
        performance_data = {
            "id": performance.id,
            "vendor": vendor_id,
            "date": performance.date,
            "on_time_delivery_rate": performance.on_time_delivery_rate,
            "quality_rating_avg": performance.quality_rating_avg,
            "average_response_time": performance.average_response_time,
            "fulfillment_rate": performance.fulfillment_rate
        }
        return JsonResponse(performance_data)
    except Vendor.DoesNotExist:
        return JsonResponse({"error": "Vendor not found"}, status=404)




from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PurchaseOrder

@api_view(['POST'])
def acknowledge_purchase_order(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response({"error": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        # Perform acknowledgment logic here
        acknowledgment_date = request.data.get('acknowledgment_date')
        if acknowledgment_date:
            purchase_order.acknowledgment_date = acknowledgment_date
            purchase_order.save()
            return Response({"message": "Purchase Order acknowledged successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Acknowledge date is required"}, status=status.HTTP_400_BAD_REQUEST)
