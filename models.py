from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SavedSearch(models.Model):
    class Type:
        HOME = "Home"
        TENANT = "Tenant"

        @classmethod
        def as_choices(cls):
            return (
                (cls.HOME, cls.HOME),
                (cls.TENANT, cls.TENANT),
            )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_type = models.CharField(max_length=10, choices=Type.as_choices())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SavedSearch for {self.user} ({self.search_type})"


class SearchCriterion(models.Model):
    saved_search = models.ForeignKey(
        SavedSearch, on_delete=models.CASCADE, related_name="criteria")
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return f"Criterion {self.key}: {self.value} for {self.saved_search}"
