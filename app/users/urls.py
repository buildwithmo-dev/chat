from django.urls import path
from . import views

urlpatterns = [
    # We remove Register, Login, Refresh, and Logout 
    # because Next.js + Supabase handle those now.
    
    # This is a placeholder for when you create a ProfileView
    # path('profile/', views.ProfileDetailView.as_view(), name='profile-detail'),
]