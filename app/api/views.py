from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import ChatGroups, Messages, Memberships
from .serializers import MessageSerializer

User = get_user_model()

class GroupHistoryView(APIView):
    # Note: You'll need to set up Supabase JWT Auth for IsAuthenticated to work
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        try:
            # Check if group exists
            group = ChatGroups.objects.get(id=group_id)
        except (ChatGroups.DoesNotExist, ValueError):
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        # Filter messages by the 'group' foreign key from your inspectdb model
        messages = Messages.objects.filter(group=group).order_by('-created_at')[:50]
        return Response(MessageSerializer(messages, many=True).data)

class AllUserChatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # 1. Find which groups the user belongs to using the Memberships table
        user_group_ids = Memberships.objects.filter(user=user).values_list('group_id', flat=True)
        
        # 2. Get the latest messages for those groups
        group_messages = Messages.objects.filter(
            group_id__in=user_group_ids
        ).order_by('-created_at')[:50]

        # 3. DM Logic
        # Your current schema only shows 'group'. If DMs are also in ChatGroups 
        # (e.g., as a group with 2 people), you can filter them here.
        # If DMs are separate, you might need a 'receiver' field in your Messages model.
        
        return Response({
            "group_messages": MessageSerializer(group_messages, many=True).data,
            # Placeholder for DMs depending on your schema setup
            "dm_messages": [], 
        })

from rest_framework import viewsets
from .models import ChatGroups
from .serializers import ChatGroupSerializer # Ensure this is in serializers.py

class ChatGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChatGroups.objects.all()
    serializer_class = ChatGroupSerializer