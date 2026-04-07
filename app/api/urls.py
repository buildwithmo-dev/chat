from django.urls import path
from . import views

urlpatterns = [
    # This is the one you were trying to visit:
    path('groups/', views.ChatGroupViewSet.as_view({'get': 'list'}), name='groups-list'),
    
    # These are already in your screenshot:
    path('messages/group/<str:group_id>/', views.GroupHistoryView.as_view(), name='group-history'),
    path('chats/', views.AllUserChatsView.as_view(), name='all-chats'),
]