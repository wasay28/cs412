from django.urls import path
from . import views
from .views import CreateProfileView, CreateStatusMessageView, UpdateProfileView

urlpatterns = [
    path('', views.profile_list, name='profile_list'),
    path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('create_status/<int:pk>/', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),
]
