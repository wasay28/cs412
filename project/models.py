from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User 

class Location(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    # Use PointField for geographic coordinates
    coordinates = models.CharField(max_length=100, blank=True, null=True, help_text="Temporary: Enter dummy coords like '0,0'")
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class JournalEntry(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        # ('friends', 'Friends Only'), # Will add later if want to implement social features
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    # Link to the User model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')
    # Link to the Location model
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='journal_entries') # Protect locations if entries exist
    # Optional image upload 
    image = models.ImageField(upload_to='journal_images/', blank=True, null=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='private')
    # ManyToMany relationship with Tag
    tags = models.ManyToManyField(Tag, blank=True, related_name='journal_entries')

    def __str__(self):
        return f"{self.title} by {self.user.username}"

