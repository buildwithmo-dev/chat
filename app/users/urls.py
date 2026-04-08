# users/urls.py
from django.urls import path
from .views import RegisterView # Make sure you import your view

urlpatterns = [
    # Add this back! 
    # Use 'register/' if you want to use the trailing slash
    path('register/', RegisterView.as_view(), name='register'), 
]