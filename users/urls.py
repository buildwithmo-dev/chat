from django.urls import path
from .views import ProfileDetailView

urlpatterns = [
    path('register/', ProfileDetailView.as_view(), name='register'),
]