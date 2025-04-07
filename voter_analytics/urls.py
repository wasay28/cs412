from django.urls import path
from . import views

urlpatterns = [
    path('', views.VoterListView.as_view(), name='voters'),
    path('voter/<str:pk>', views.VoterDetailView.as_view(), name='voter'),
]
