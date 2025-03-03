from django.shortcuts import render, get_object_or_404
from .models import Profile, StatusMessage

# Create your views here.
def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'mini_fb/profile_list.html', {'profiles': profiles})

def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    status_messages = profile.get_status_messages()
    return render(request, 'mini_fb/profile_detail.html', {'profile': profile, 'status_messages': status_messages})