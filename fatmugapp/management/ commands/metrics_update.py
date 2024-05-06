import time  # Import the time module for the sleep function

from django.core.management.base import BaseCommand

from fatmugpro.fatmugapp.models import Vendor


class Command(BaseCommand):
    help = 'Update metrics for all vendors every 3 seconds'

    def handle(self, *args, **options):
        while True:
            vendors = Vendor.objects.all()
            for vendor in vendors:
                vendor.update_metrics()  # Call your update_metrics method
            self.stdout.write(self.style.SUCCESS('Metrics updated for all vendors'))
            time.sleep(3)  # Wait for 3 seconds before running again
