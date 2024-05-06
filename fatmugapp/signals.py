import logging
from django.db.models.signals import post_save
from django.dispatch import receiver




logger = logging.getLogger(__name__)

@receiver(post_save, sender='fatmugapp.Vendor')
def update_related_performance(sender, instance, **kwargs):
    from .models import HistoricalPerformance  # Import moved inside the function
    for performance in instance.historicalperformance_set.all():
        performance.save()

