from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import SavedSearchForm, SearchCriterionForm
from .mixins import UserIsOwnerMixin
from .models import SavedSearch, SearchCriterion


class SavedSearchListView(LoginRequiredMixin, ListView):
    model = SavedSearch
    template_name = "savedsearch_list.html"

    def get_queryset(self):
        return SavedSearch.objects.filter(user=self.request.user)


class SavedSearchDetailView(LoginRequiredMixin, UserIsOwnerMixin, DetailView):
    model = SavedSearch
    template_name = "savedsearch_detail.html"


class SavedSearchCreateView(LoginRequiredMixin, CreateView):
    model = SavedSearch
    form_class = SavedSearchForm
    template_name = "savedsearch_form.html"
    success_url = reverse_lazy("savedsearch-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SavedSearchUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = SavedSearch
    form_class = SavedSearchForm
    template_name = "savedsearch_form.html"
    success_url = reverse_lazy("savedsearch-list")


class SavedSearchDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = SavedSearch
    template_name = "savedsearch_delete.html"
    success_url = reverse_lazy("savedsearch-list")


class SearchCriterionCreateView(LoginRequiredMixin, CreateView):
    model = SearchCriterion
    form_class = SearchCriterionForm
    template_name = "searchcriterion_form.html"
    success_url = reverse_lazy("savedsearch-list")
