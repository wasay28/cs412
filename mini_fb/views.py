from django.shortcuts import render, get_object_or_404
from .models import Profile, StatusMessage
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CreateProfileForm, CreateStatusMessageForm

# Create your views here.
def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'mini_fb/profile_list.html', {'profiles': profiles})

def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    status_messages = profile.get_status_messages()
    return render(request, 'mini_fb/profile_detail.html', {'profile': profile, 'status_messages': status_messages})

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    success_url = reverse_lazy('profile_list')

class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        profile_id = self.kwargs['pk']
        form.instance.profile_id = profile_id
        return super().form_valid(form)

    def get_success_url(self):
        profile_id = self.kwargs['pk']
        return reverse_lazy('profile_detail', kwargs={'pk': profile_id})