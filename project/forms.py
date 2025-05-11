from django import forms
from .models import JournalEntry, Location

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        # Include fields users should fill out
        # Exclude 'user' because we set it automatically in the view
        fields = ['title', 'content', 'location', 'tags', 'image']
        

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'description', 'latitude', 'longitude', 'country', 'city']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
