import uuid
from django.db import connection
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChatGroups, Memberships, Messages
from .serializers import ChatGroupSerializer, MessageSerializer, SendMessageSerializer


def _serialize_messages(messages):
    return MessageSerializer(messages, many=True).data


class GroupHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        if not Memberships.objects.filter(group_id=group_id, user_id=request.user.id).exists():
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        messages = Messages.objects.filter(group_id=group_id).order_by("created_at")[:100]
        return Response(_serialize_messages(messages))


class AllUserChatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        group_ids = Memberships.objects.filter(user_id=request.user.id).values_list("group_id", flat=True)
        messages = Messages.objects.filter(group_id__in=group_ids).order_by("created_at")[:200]
        return Response(_serialize_messages(messages))


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        group_id = data.get("group_id")

        if group_id:
            if not Memberships.objects.filter(group_id=group_id, user_id=request.user.id).exists():
                return Response({"error": "You are not a member of this group"}, status=status.HTTP_403_FORBIDDEN)
        else:
            membership = Memberships.objects.filter(user_id=request.user.id).first()
            if not membership:
                return Response({"error": "No chat group is available for this account"}, status=status.HTTP_400_BAD_REQUEST)
            group_id = membership.group_id

        message = Messages.objects.create(
            id=uuid.uuid4(),
            sender_id=request.user.id,
            group_id=group_id,
            content=data["text"],
            attachments=data.get("attachments"),
            created_at=timezone.now(),
        )
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


class ChatGroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChatGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        group_ids = Memberships.objects.filter(user_id=self.request.user.id).values_list("group_id", flat=True)
        return ChatGroups.objects.filter(id__in=group_ids).order_by("name")
