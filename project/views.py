# Create your views here.

from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin # To protect create views

from .models import JournalEntry, Location, Tag
from .forms import JournalEntryForm, LocationForm 

# --- Journal Entry Views ---

class JournalEntryListView(generic.ListView):
    model = JournalEntry
    context_object_name = 'journalentry_list' # Default is 'object_list'
    template_name = 'travelbuddy/journalentry_list.html' # Explicitly state template
    # Optional: Order by most recent
    queryset = JournalEntry.objects.order_by('-created_date')

class JournalEntryDetailView(generic.DetailView):
    model = JournalEntry
    context_object_name = 'journalentry' # Default is 'object' or 'journalentry'
    template_name = 'travelbuddy/journalentry_detail.html'

class JournalEntryCreateView(LoginRequiredMixin, generic.CreateView):
    model = JournalEntry
    form_class = JournalEntryForm 
    template_name = 'travelbuddy/journalentry_form.html'
    success_url = reverse_lazy('travelbuddy:entry-list') # Redirect after successful creation

    # Automatically set the user to the logged-in user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# --- Location Views ---

class LocationListView(generic.ListView):
    model = Location
    context_object_name = 'location_list'
    template_name = 'travelbuddy/location_list.html'
    queryset = Location.objects.order_by('name')

class LocationDetailView(generic.DetailView):
    model = Location
    context_object_name = 'location'
    template_name = 'travelbuddy/location_detail.html'

class LocationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Location
    form_class = LocationForm # Use the ModelForm we will create
    template_name = 'travelbuddy/location_form.html'
    success_url = reverse_lazy('travelbuddy:location-list')


