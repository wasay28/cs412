from django.shortcuts import render, get_object_or_404
from .models import Profile, StatusMessage, Image, StatusImage
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm

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
    
    def get_success_url(self):
        # Redirect to the newly created profile's detail page
        return self.object.get_absolute_url()

class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        # Save the status message to the database
        sm = form.save(commit=False)
        sm.profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        sm.save()

        # Process uploaded files
        files = self.request.FILES.getlist('files')  # Get list of uploaded files
        for f in files:
            # Create and save an Image object
            img = Image(profile=sm.profile, image_file=f)
            img.save()

            # Create and save a StatusImage object linking the image to the status message
            status_image = StatusImage(status_message=sm, image=img)
            status_image.save()

        return super().form_valid(form)

    def get_success_url(self):
        profile_id = self.kwargs['pk']
        return reverse_lazy('profile_detail', kwargs={'pk': profile_id})

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    
    def get_success_url(self):
        # Redirect to profile detail page after successful update
        return reverse_lazy('profile_detail', kwargs={'pk': self.object.pk})