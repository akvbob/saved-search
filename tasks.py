from celery.task import task
from datetime import datetime, timedelta

from .models import HomeListing, TenantListing
from .services import process_listings


@task
def process_new_listings():
    day_before = datetime.now() - timedelta(hours=24)

    new_home_listings = HomeListing.objects.filter(created_at__gte=day_before)
    process_listings(new_home_listings, HomeListing)

    new_tenant_listings = TenantListing.objects.filter(created_at__gte=day_before)
    process_listings(new_tenant_listings, TenantListing)
