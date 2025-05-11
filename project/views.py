# Create your views here.

from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # To protect create views
from django.contrib import messages
from django.shortcuts import redirect

from django.db.models import Q

from .models import JournalEntry, Location, Tag
from .forms import JournalEntryForm, LocationForm 

# --- Journal Entry Views ---

class JournalEntryListView(generic.ListView):
    model = JournalEntry
    context_object_name = 'journalentry_list' # Default is 'object_list'
    template_name = 'project/journalentry_list.html' # Explicitly state template
    # Optional: Order by most recent
    def get_queryset(self):
        queryset = JournalEntry.objects.order_by('-created_date') # Start with default ordering
        query = self.request.GET.get('q')
        if query:
            # Search in title, content, user's username, location name, or tags
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__username__icontains=query) |
                Q(location__name__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct() # Use distinct because of ManyToMany join with tags
        return queryset

class JournalEntryDetailView(generic.DetailView):
    model = JournalEntry
    context_object_name = 'journalentry' # Default is 'object' or 'journalentry'
    template_name = 'project/journalentry_detail.html'

class JournalEntryCreateView(LoginRequiredMixin, generic.CreateView):
    model = JournalEntry
    form_class = JournalEntryForm 
    template_name = 'project/journalentry_form.html'
    success_url = reverse_lazy('project:entry-list') # Redirect after successful creation

    # Automatically set the user to the logged-in user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class JournalEntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = JournalEntry
    form_class = JournalEntryForm 
    template_name = 'project/journalentry_form.html' 
    # success_url = reverse_lazy('project:entry-list') # Or redirect to detail view

    def get_success_url(self):
        # Redirect back to the detail view of the updated entry
        return reverse_lazy('project:entry-detail', kwargs={'pk': self.object.pk})

    # Test function to ensure only the author can edit their entry
    def test_func(self):
        entry = self.get_object()
        return self.request.user == entry.user

class JournalEntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = JournalEntry
    template_name = 'project/journalentry_confirm_delete.html' 
    success_url = reverse_lazy('project:entry-list') # Redirect to list after delete

    # Test function to ensure only the author can delete their entry
    def test_func(self):
        entry = self.get_object()
        return self.request.user == entry.user

# --- Location Views ---

class LocationListView(generic.ListView):
    model = Location
    context_object_name = 'location_list'
    template_name = 'project/location_list.html'
    def get_queryset(self):
        queryset = Location.objects.order_by('name')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(country__icontains=query) |
                Q(city__icontains=query) |
                Q(address__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass all locations with lat/lng for the map
        context['locations_for_map'] = Location.objects.exclude(latitude__isnull=True, longitude__isnull=True)
        return context

class LocationDetailView(generic.DetailView):
    model = Location
    context_object_name = 'location'
    template_name = 'project/location_detail.html'

class LocationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Location
    form_class = LocationForm 
    template_name = 'project/location_form.html'
    success_url = reverse_lazy('project:location-list')

class LocationUpdateView(LoginRequiredMixin, generic.UpdateView): 
    model = Location
    form_class = LocationForm
    template_name = 'project/location_form.html'
    # success_url = reverse_lazy('project:location-list')

    def get_success_url(self):
        return reverse_lazy('project:location-detail', kwargs={'pk': self.object.pk})

class LocationDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Location
    template_name = 'project/location_confirm_delete.html'
    success_url = reverse_lazy('project:location-list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Check if any journal entries reference this location
        if self.object.journalentry_set.exists():
            messages.error(request, 'Cannot delete this location because one or more journal entries reference it. Please reassign or delete those entries first.')
            return redirect('project:location-detail', pk=self.object.pk)
        return super().dispatch(request, *args, **kwargs)


