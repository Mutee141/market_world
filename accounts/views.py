from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsOwnerOrManager
from .models import User
from .serializers import UserSerializer, StaffCreateSerializer


class MeView(APIView):
    """Frontend calls this right after login to know role/store and decide what to render."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class StaffViewSet(viewsets.ModelViewSet):
    """Owner/Manager manages their store's staff accounts."""
    permission_classes = [IsOwnerOrManager]

    def get_queryset(self):
        return User.objects.filter(store=self.request.store).exclude(role='super_admin')

    def get_serializer_class(self):
        return StaffCreateSerializer if self.action == 'create' else UserSerializer

    def perform_create(self, serializer):
        serializer.save(store=self.request.store)