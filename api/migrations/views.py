import uuid

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Profiles

from .models import ChatGroups, Memberships, Messages
from .serializers import ChatGroupSerializer, MessageSerializer, SendMessageSerializer

DEFAULT_LIMIT, MAX_LIMIT = 50, 100


def _page(qs, request):
    """Newest-N page (optionally older than ?before=), returned oldest-first."""
    try:
        limit = max(1, min(int(request.query_params.get("limit", DEFAULT_LIMIT)), MAX_LIMIT))
    except ValueError:
        limit = DEFAULT_LIMIT
    before = parse_datetime(request.query_params.get("before", "") or "")
    if before:
        qs = qs.filter(created_at__lt=before)
    rows = list(qs.order_by("-created_at")[:limit])
    rows.reverse()
    return rows


def _serialize(messages):
    ids = {m.sender_id for m in messages if m.sender_id}
    profiles = {p.id: p for p in Profiles.objects.filter(id__in=ids)}
    return MessageSerializer(messages, many=True, context={"profiles": profiles}).data


def _is_member(request, group_id):
    return Memberships.objects.filter(group_id=group_id, user_id=request.user.id).exists()


class GroupHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        if not _is_member(request, group_id):
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(_serialize(_page(Messages.objects.filter(group_id=group_id), request)))


class AllUserChatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        group_ids = Memberships.objects.filter(user_id=request.user.id).values_list("group_id", flat=True)
        return Response(_serialize(_page(Messages.objects.filter(group_id__in=group_ids), request)))


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        group_id = data.get("group_id")

        if group_id:
            if not _is_member(request, group_id):
                return Response({"error": "You are not a member of this group"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            membership = Memberships.objects.filter(user_id=request.user.id).first()
            if not membership:
                return Response({"error": "No chat group is available for this account"},
                                status=status.HTTP_400_BAD_REQUEST)
            group_id = membership.group_id

        message = Messages.objects.create(
            id=uuid.uuid4(),
            sender_id=request.user.id,
            group_id=group_id,
            content=data["text"],
            attachments=data.get("attachments"),
            created_at=timezone.now(),
        )
        ctx = {"profiles": {request.user.id: request.user}}
        return Response(MessageSerializer(message, context=ctx).data, status=status.HTTP_201_CREATED)


class ChatGroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChatGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        group_ids = Memberships.objects.filter(user_id=self.request.user.id).values_list("group_id", flat=True)
        return ChatGroups.objects.filter(id__in=group_ids).order_by("name")
