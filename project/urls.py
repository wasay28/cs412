from django.urls import path
from . import views

app_name = 'project' 

urlpatterns = [
    # Journal Entry URLs
    path('', views.JournalEntryListView.as_view(), name='entry-list'), # Homepage shows entries
    path('entry/<int:pk>/', views.JournalEntryDetailView.as_view(), name='entry-detail'),
    path('entry/new/', views.JournalEntryCreateView.as_view(), name='entry-create'),
    path('entry/<int:pk>/edit/', views.JournalEntryUpdateView.as_view(), name='entry-update'),
    path('entry/<int:pk>/delete/', views.JournalEntryDeleteView.as_view(), name='entry-delete'),

    # Location URLs
    path('locations/', views.LocationListView.as_view(), name='location-list'),
    path('location/<int:pk>/', views.LocationDetailView.as_view(), name='location-detail'),
    path('location/new/', views.LocationCreateView.as_view(), name='location-create'),
    path('location/<int:pk>/edit/', views.LocationUpdateView.as_view(), name='location-update'),
    path('location/<int:pk>/delete/', views.LocationDeleteView.as_view(), name='location-delete'),



    
]
