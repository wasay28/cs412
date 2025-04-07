from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render
from .models import Voter
import datetime
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import pandas as pd

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

class GraphsView(TemplateView):
    """
    Display graphs of aggregate data about Voter records.
    
    This view creates and displays three graphs:
    1. A histogram of voters by year of birth
    2. A pie chart of voters by party affiliation
    3. A histogram of voter participation in each election
    """
    template_name = 'voter_analytics/graphs.html'
    
    def get_context_data(self, **kwargs):
        """
        Create graph visualizations and add them to the context.
        
        Returns:
            dict: Context data including the HTML representations of the graphs.
        """
        context = super().get_context_data(**kwargs)
        
        # Apply filters from request parameters
        voters = Voter.objects.all()
        
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
            voters = voters.filter(party_affiliation__iexact=party.strip())
            
        if min_year:
            min_date = datetime.date(int(min_year), 1, 1)
            voters = voters.filter(date_of_birth__gte=min_date)
            
        if max_year:
            max_date = datetime.date(int(max_year), 12, 31)
            voters = voters.filter(date_of_birth__lte=max_date)
            
        if voter_score and voter_score != 'all':
            voters = voters.filter(voter_score=int(voter_score))
            
        # Filter by election participation
        if v20state == 'on':
            voters = voters.filter(v20state=True)
            
        if v21town == 'on':
            voters = voters.filter(v21town=True)
            
        if v21primary == 'on':
            voters = voters.filter(v21primary=True)
            
        if v22general == 'on':
            voters = voters.filter(v22general=True)
            
        if v23town == 'on':
            voters = voters.filter(v23town=True)
        
        # Create the graphs
        birth_year_graph = self.create_birth_year_histogram(voters)
        party_graph = self.create_party_pie_chart(voters)
        election_graph = self.create_election_histogram(voters)
        
        # Add graphs to context
        context['birth_year_graph'] = birth_year_graph
        context['party_graph'] = party_graph
        context['election_graph'] = election_graph
        
        # Add filter options to context (reuse from VoterListView)
        parties = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        parties = sorted([p.strip() for p in parties if p])
        
        current_year = datetime.datetime.now().year
        years = list(range(current_year - 100, current_year + 1))
        
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
    
    def create_birth_year_histogram(self, voters):
        """
        Create a histogram showing the distribution of voters by birth year.
        
        Args:
            voters: QuerySet of Voter objects
            
        Returns:
            str: HTML representation of the graph
        """
        # Extract birth years
        birth_years = [voter.date_of_birth.year for voter in voters]
        
        # Create histogram
        fig = px.histogram(
            x=birth_years,
            title=f"Voter Distribution by Year of Birth (n={len(birth_years)})",
            labels={'x': 'Year of Birth', 'y': 'Count'},
            nbins=100
        )
        
        # Customize layout
        fig.update_layout(
            xaxis_title="Year of Birth",
            yaxis_title="Number of Voters",
            plot_bgcolor='rgba(240, 240, 250, 0.2)'
        )
        
        return fig.to_html(full_html=False)
    
    def create_party_pie_chart(self, voters):
        """
        Create a pie chart showing the distribution of voters by party affiliation.
        
        Args:
            voters: QuerySet of Voter objects
            
        Returns:
            str: HTML representation of the graph
        """
        # Count party affiliations
        party_counts = Counter([voter.party_affiliation.strip() for voter in voters])
        
        # Create pie chart
        fig = px.pie(
            values=list(party_counts.values()),
            names=list(party_counts.keys()),
            title=f"Voter Distribution by Party Affiliation (n={len(voters)})"
        )
        
        # Customize layout
        fig.update_layout(
            legend_title="Party",
        )
        
        return fig.to_html(full_html=False)
    
    def create_election_histogram(self, voters):
        """
        Create a histogram showing voter participation in each election.
        
        Args:
            voters: QuerySet of Voter objects
            
        Returns:
            str: HTML representation of the graph
        """
        # Count participation in each election
        v20state_count = sum(1 for voter in voters if voter.v20state)
        v21town_count = sum(1 for voter in voters if voter.v21town)
        v21primary_count = sum(1 for voter in voters if voter.v21primary)
        v22general_count = sum(1 for voter in voters if voter.v22general)
        v23town_count = sum(1 for voter in voters if voter.v23town)
        
        # Create data for the bar chart
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        counts = [v20state_count, v21town_count, v21primary_count, v22general_count, v23town_count]
        
        # Create bar chart
        fig = go.Figure(data=[
            go.Bar(x=elections, y=counts)
        ])
        
        # Customize layout
        fig.update_layout(
            title=f"Vote Count by Election (n={len(voters)})",
            xaxis_title="Election",
            yaxis_title="Number of Voters",
            plot_bgcolor='rgba(240, 240, 250, 0.2)'
        )
        
        return fig.to_html(full_html=False)