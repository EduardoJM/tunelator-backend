from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from mails.models import UserMail
from mails.serializers import UserMailSerializer, UserMailRetrieveSerializer

class UserMailViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "created_at": ["gte", "lte", "exact", "gt", "lt"],
        "updated_at": ["gte", "lte", "exact", "gt", "lt"],
        "plan_enabled": ["exact"],
        "redirect_enabled": ["exact"],
    }
    search_fields = ["mail", "name"]
    ordering = ["-updated_at"]
    serializer_class = UserMailSerializer

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return UserMailRetrieveSerializer
        return UserMailSerializer

    def get_queryset(self):
        user = self.request.user
        return UserMail.objects.filter(user=user).all()
