# saved-search

## How the saved search criteria would be modelled and persisted in the database

In task mentioned that project will scale to hundreds of thousands or millions of active listings. So I decided to use normalized data structure in this case. It Separates related models for storing search criteria. Each criterion is stored as a key-value pair in a related model, which allows for better indexing and more complex queries. This structure supports highly optimized queries at the cost of increased complexity in managing the data.

**Model classes**:
1. `SavedSearch`: represents a saved search associated with a user. Also it has an attribute for search_type (Tenant/Home)
2. `SearchCriterion`: stores individual criteria for saved searches, such as municipality or rent_amount. It has attributes for key, value, and a foreign key to SavedSearch.

See: `models.py` file for an example of these models.

## How to relate a listing match to a saved search given the different Listings classes
Each SavedSearch has a search_type field that indicates whether it applies to HomeListing or TenantListing. To handle different attributes across different listing classes, use `listing_model._meta.get_fields()` function.

See: `services.py`.

## What kind of views and permissions would be needed to manage the saved searches and what security implications would need to be considered

Views for managing saved searches:
    - SavedSearchListView,
    - SavedSearchDetailView,
    - SavedSearchCreateView,
    - SavedSearchUpdateView,
    - SavedSearchDeleteView,
    - SearchCriterionCreateView

**Permissions:**
- Need to ensure that users can only see/manage their own saved searches and criteria.
- Also Anonymous User should not have access to SavedSearch or SavedSearchCriterion

See: `views.py` and `mixins.py`.

## How newly published listings would be processed to identify matches for any saved search

- Create a celery task that runs for instance once every day
- Filter home and tenant listings that was created during the time this celery task was runned the last time
- Process both listings - compare them against saved searches
- If matching saved search exist - notify the user of SavedSearch

See: `tasks.py`.

## Strategies for reducing potential notification noise in the event of many listings match a particular search, we do not want to flood the user with email

Possible strategies:
- Limit the number of emails sent per user per day (don't send an email each time when new listing appeared)
- Send a summary email with all matches collected over some period of time
- Allow users to configure their notification frequency and preferences.

## Further improvements:
- In-App Notifications or SMS notifications
- fuzzy matching
- machine learning recommendation system based on user behaviour

## Important Note
The code provided in this repository is intended for illustrative purposes only and is not a fully functional project. It serves as an example of how the saved search feature can be implemented using Django. It is not runnable project.