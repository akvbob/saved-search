from django.db.models import Q
from django.core import mail
from .models import SavedSearch
from .models import SearchCriterion


def match_listings_with_saved_searches(listing, listing_model):
    matched_searches = []
    saved_searches = SavedSearch.objects.filter(
        search_type=listing_model.__name__)

    for search in saved_searches:
        criteria = SearchCriterion.objects.filter(saved_search=search)
        query = build_query_from_criteria(criteria, listing_model)

        # Check if the listing matches the saved search criteria
        if listing_model.objects.filter(query).filter(id=listing.id).exists():
            matched_searches.append(search)
    return matched_searches


def build_query_from_criteria(criteria, listing_model):
    query = Q()
    for criterion in criteria:
        if criterion.key in [field.name for field in listing_model._meta.get_fields()]:
            query &= Q(**{criterion.key: criterion.value})
    return query


def send_email_notification(user, listings):
    subject = "New listings matching your saved search"
    message = f"Hi {user.username},\n\nHere are some new listings that match your saved search:\n"
    for listing in listings:
        message += f"- {listing.title}\n"
    mail.send_mail(subject, message, "from@example.com", [user.email])


def process_listings(listings_queryset, listing_model):
    for listing in listings_queryset:
        matched_searches = match_listings_with_saved_searches(listing, listing_model)
        for search in matched_searches:
            send_email_notification(search.user, listing)
