from rest_framework import viewsets, filters, mixins, decorators, response, status
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from mails.models import UserMail, UserReceivedMail
from mails.serializers import (
    UserMailSerializer,
    UserMailRetrieveSerializer,
    UserReceivedMailSerializer,
)

class UserReceivedMailViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "date": ["gte", "lte", "exact", "gt", "lt"],
        "delivered_date": ["gte", "lte", "exact", "gt", "lt"],
        "delivered": ["exact"],
        "mail": ["exact"],
    }
    search_fields = ["origin_mail", "subject"]
    ordering = ["-date"]
    serializer_class = UserReceivedMailSerializer

    @decorators.action(methods=["POST"], detail=True)
    def resend(self, request):
        received_mail = self.get_object()
        if not received_mail:
            return response.Response({
                'detail': _('Received mail not found.')
            }, status=status.HTTP_404_NOT_FOUND)
        
        from mails.tasks import send_redirect_mail
        send_redirect_mail.apply_async(args=[received_mail.id, True], coutdown=2)
        
        return response.Response()

    def get_queryset(self):
        user = self.request.user
        return UserReceivedMail.objects.filter(mail__user=user).all()

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
