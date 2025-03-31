from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, StatusMessage, Image, StatusImage
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.views import View
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'mini_fb/profile_list.html', {'profiles': profiles})

@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    status_messages = profile.get_status_messages()
    return render(request, 'mini_fb/profile_detail.html', {'profile': profile, 'status_messages': status_messages})

class CreateProfileView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    
    def get_success_url(self):
        # Redirect to the newly created profile's detail page
        return self.object.get_absolute_url()

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
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

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    
    def get_success_url(self):
        # Redirect to profile detail page after successful update
        return reverse_lazy('profile_detail', kwargs={'pk': self.object.pk})

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status'
    
    def get_success_url(self):
        # Redirect to the profile page after successful deletion
        profile_id = self.object.profile.id
        return reverse_lazy('profile_detail', kwargs={'pk': profile_id})

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status'
    
    def get_success_url(self):
        # Redirect to the profile page after successful update
        profile_id = self.object.profile.id
        return reverse_lazy('profile_detail', kwargs={'pk': profile_id})

class AddFriendView(View):
    def get(self, request, profile_pk, friend_pk):
        # Get the profile doing the friending
        profile = get_object_or_404(Profile, pk=profile_pk)
        # Get the profile to be friended
        friend = get_object_or_404(Profile, pk=friend_pk)
        
        # Add the friend
        profile.add_friend(friend)
        
        # Redirect back to the profile page
        return redirect(reverse('profile_detail', kwargs={'pk': profile_pk}))
    
def friend_suggestions(request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        suggestions = profile.get_friend_suggestions()
        return render(request, 'mini_fb/friend_suggestions.html', 
                    {'profile': profile, 'suggestions': suggestions})

class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['news_feed'] = profile.get_news_feed()
        return context
