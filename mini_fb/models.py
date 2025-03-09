from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_status_messages(self):
        return self.status_messages.all().order_by('-timestamp')
    
    def get_absolute_url(self):
        # Use reverse to dynamically generate the profile detail URL
        return reverse('profile_detail', kwargs={'pk': self.pk})
    
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="status_messages")

    def __str__(self):
        return f"Message by {self.profile.first_name} at {self.timestamp}"