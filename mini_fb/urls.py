from django.urls import path
from . import views
from .views import CreateProfileView, CreateStatusMessageView

urlpatterns = [
    path('', views.profile_list, name='profile_list'),
    path('<int:pk>/', views.profile_detail, name='profile_detail'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
]
