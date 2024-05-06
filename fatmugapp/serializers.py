from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    # Explicitly define read-only fields if they are computed within the model or through methods
    on_time_delivery_rate = serializers.FloatField(read_only=True)
    quality_rating_avg = serializers.FloatField(read_only=True)
    average_response_time = serializers.FloatField(read_only=True)
    fulfillment_rate = serializers.FloatField(read_only=True)

    class Meta:
        model = Vendor
        fields = '__all__'  # This includes all model fields in the serializer
        # Specify any fields that should not be modified directly via the API
        read_only_fields = ('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')

    def validate_contact_details(self, value):
        """
        Custom validation for contact details to ensure it includes an email and phone number.
        """
        if "@" not in value:
            raise serializers.ValidationError("Contact details must include an email.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Contact details must include a phone number.")
        return value

    def update(self, instance, validated_data):
        """
        Custom update logic that might include handling side effects or recalculations.
        """
        instance = super().update(instance, validated_data)
        # Assume update_metrics() recalculates and saves metrics based on other fields
        instance.update_metrics()  # Make sure this method exists in your model
        instance.save()  # Ensure all changes, including recalculations, are saved
        return instance

    # If needed, define a create method as well
    def create(self, validated_data):
        """
        Custom create logic, especially useful if certain fields need initialization beyond the default field values.
        """
        instance = Vendor.objects.create(**validated_data)
        instance.update_metrics()  # Optional: compute metrics upon creation
        instance.save()
        return instance



from rest_framework import serializers
from .models import PurchaseOrder

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


from rest_framework import serializers
from .models import HistoricalPerformance

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = ['id', 'vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
