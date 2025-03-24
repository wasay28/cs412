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
    
    def get_friends(self):
    # Get all friendship relationships where this profile is either profile1 or profile2
        friends_as_profile1 = Friend.objects.filter(profile1=self)
        friends_as_profile2 = Friend.objects.filter(profile2=self)
        
        # Create a list to store the friend profiles
        friend_profiles = []
        
        # Add the opposite profile from each friendship relationship
        for friendship in friends_as_profile1:
            friend_profiles.append(friendship.profile2)
        
        for friendship in friends_as_profile2:
            friend_profiles.append(friendship.profile1)
        
        return friend_profiles
    
    def add_friend(self, other):
        # Check if friendship already exists (in either direction)
        if Friend.objects.filter(profile1=self, profile2=other).exists() or \
        Friend.objects.filter(profile1=other, profile2=self).exists():
            # Friendship already exists, do nothing
            return False
        
        # Check that we're not trying to friend ourselves
        if self == other:
            return False
            
        # Create new friendship
        friendship = Friend(profile1=self, profile2=other)
        friendship.save()
        return True
    
    def get_friend_suggestions(self):
        # Get all profiles
        all_profiles = Profile.objects.exclude(id=self.id)
        
        # Get existing friends
        friends = self.get_friends()
        
        # Exclude existing friends from all profiles
        friend_suggestions = [profile for profile in all_profiles if profile not in friends]
        
        return friend_suggestions
    
    def get_news_feed(self):
        # Get all friends of this profile
        friends = self.get_friends()
        
        # Start with this profile's own status messages
        news_feed = list(self.get_status_messages())
        
        # Add all status messages from friends
        for friend in friends:
            news_feed.extend(list(friend.get_status_messages()))
        
        # Sort all status messages by timestamp, most recent first
        news_feed.sort(key=lambda x: x.timestamp, reverse=True)
        
        return news_feed



class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="status_messages")

    def __str__(self):
        return f"Message by {self.profile.first_name} at {self.timestamp}"
    
    def get_images(self):
        return self.status_images.all()
    
class Image(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="images")
    image_file = models.ImageField(upload_to='images/')  # Store images in 'media/images/'
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Image for {self.profile.first_name} uploaded at {self.timestamp}"

class StatusImage(models.Model):
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE, related_name="status_images")
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for StatusMessage ID {self.status_message.id}"
    
class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, related_name="friends_as_profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name="friends_as_profile2", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile1} is friends with {self.profile2} since {self.timestamp}"
