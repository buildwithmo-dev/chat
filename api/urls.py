from django.urls import path
from . import views

urlpatterns = [
    path("groups/", views.ChatGroupViewSet.as_view({"get": "list"}), name="groups-list"),
    path("messages/group/<uuid:group_id>/", views.GroupHistoryView.as_view(), name="group-history"),
    path("messages/allchats/", views.AllUserChatsView.as_view(), name="all-chats"),
    path("messages/send/", views.SendMessageView.as_view(), name="send-message"),
]
