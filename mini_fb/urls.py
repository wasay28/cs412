from django.urls import path
from . import views
from .views import CreateProfileView, CreateStatusMessageView, UpdateProfileView, UpdateStatusMessageView, DeleteStatusMessageView, AddFriendView, ShowNewsFeedView

urlpatterns = [
    path('', views.profile_list, name='profile_list'),
    path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('create_status/<int:pk>/', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status'),
    path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('profile/<int:profile_pk>/add_friend/<int:friend_pk>/', AddFriendView.as_view(), name='add_friend'),
    path('profile/<int:pk>/friend_suggestions/', views.friend_suggestions, name='friend_suggestions'),
    path('profile/<int:pk>/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),
]
