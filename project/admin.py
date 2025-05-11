from django.contrib import admin

# Register your models here.

from .models import Location, Tag, JournalEntry

# Register models to make them available in the admin interface
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin): 
    list_display = ('name', 'city', 'country', 'latitude', 'longitude')
    search_fields = ('name', 'city', 'country', 'address')
    list_filter = ('country', 'city')
  

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'location', 'created_date', 'visibility')
    list_filter = ('visibility', 'created_date', 'user', 'tags')
    search_fields = ('title', 'content', 'user__username', 'location__name')
    # Add filter_horizontal for easier tag selection if you have many tags
    filter_horizontal = ('tags',)
    # Make foreign key fields searchable popups instead of dropdowns
    raw_id_fields = ('user', 'location',)
    date_hierarchy = 'created_date'

