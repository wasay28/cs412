from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import Voter
import datetime

# Create your views here.
class VoterListView(ListView):
    """
    Display a paginated list of voters with filtering capabilities.
    
    This view shows voter records with pagination and allows filtering by
    party affiliation, date of birth range, voter score, and voting history.
    """
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100
    
    def get_queryset(self):
        """
        Return a filtered queryset of voters based on the request parameters.
        
        Returns:
            QuerySet: A filtered queryset of Voter objects.
        """
        queryset = Voter.objects.all()
        
        # Get filter parameters from request
        party = self.request.GET.get('party')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')
        
        # Apply filters if they exist
        if party and party != 'all':
            queryset = queryset.filter(party_affiliation__iexact=party.strip())
            
        if min_year:
            min_date = datetime.date(int(min_year), 1, 1)
            queryset = queryset.filter(date_of_birth__gte=min_date)
            
        if max_year:
            max_date = datetime.date(int(max_year), 12, 31)
            queryset = queryset.filter(date_of_birth__lte=max_date)
            
        if voter_score and voter_score != 'all':
            queryset = queryset.filter(voter_score=int(voter_score))
            
        # Filter by election participation
        if v20state == 'on':
            queryset = queryset.filter(v20state=True)
            
        if v21town == 'on':
            queryset = queryset.filter(v21town=True)
            
        if v21primary == 'on':
            queryset = queryset.filter(v21primary=True)
            
        if v22general == 'on':
            queryset = queryset.filter(v22general=True)
            
        if v23town == 'on':
            queryset = queryset.filter(v23town=True)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.
        
        Returns:
            dict: Context data including filter options.
        """
        context = super().get_context_data(**kwargs)
        
        # Get unique party affiliations for the dropdown
        parties = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        parties = sorted([p.strip() for p in parties if p])
        
        # Generate year ranges for date of birth dropdowns
        current_year = datetime.datetime.now().year
        years = list(range(current_year - 100, current_year + 1))
        
        # Add filter options to context
        context['parties'] = parties
        context['years'] = years
        context['voter_scores'] = list(range(6))  # 0-5 scores
        
        # Preserve filter selections
        context['selected_party'] = self.request.GET.get('party', '')
        context['selected_min_year'] = self.request.GET.get('min_year', '')
        context['selected_max_year'] = self.request.GET.get('max_year', '')
        context['selected_voter_score'] = self.request.GET.get('voter_score', '')
        context['selected_v20state'] = self.request.GET.get('v20state', '') == 'on'
        context['selected_v21town'] = self.request.GET.get('v21town', '') == 'on'
        context['selected_v21primary'] = self.request.GET.get('v21primary', '') == 'on'
        context['selected_v22general'] = self.request.GET.get('v22general', '') == 'on'
        context['selected_v23town'] = self.request.GET.get('v23town', '') == 'on'
        
        return context


class VoterDetailView(DetailView):
    """
    Display detailed information about a single voter.
    
    This view shows all fields for a specific voter, including personal information
    and voting history.
    """
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'
    pk_url_kwarg = 'pk'
