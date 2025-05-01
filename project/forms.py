

from django import forms
from .models import JournalEntry, Location

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        # Include fields users should fill out
        # Exclude 'user' because we set it automatically in the view
        fields = ['title', 'content', 'location', 'visibility', 'tags', 'image']
        

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'description', 'coordinates', 'country', 'city', 'address']
        # Help text is already in the model for coordinates
