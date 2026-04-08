# users/urls.py
from django.urls import path
from .views import ProfileDetailView # We'll use your Profile view as the endpoint

urlpatterns = [
    # This maps the URL your React app is hitting to your Profile view
    path('register/', ProfileDetailView.as_view(), name='register'), 
]