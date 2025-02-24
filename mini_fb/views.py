from django.shortcuts import render
from .models import Profile

# Create your views here.
def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'mini_fb/profile_list.html', {'profiles': profiles})

def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'mini_fb/profile_detail.html', {'profile': profile})