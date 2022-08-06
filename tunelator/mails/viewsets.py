from rest_framework import viewsets, filters, mixins, decorators, response, status
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from mails.models import UserMail, UserReceivedMail
from mails.serializers import (
    UserMailSerializer,
    UserMailRetrieveSerializer,
    UserReceivedMailSerializer,
)
from docs.responses import (
    NotFoundResponse,
    UnauthenticatedResponse,
    create_bad_request_response,
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

    @swagger_auto_schema(
        request_body=None,
        responses={
            status.HTTP_200_OK: 'No Body',
            status.HTTP_401_UNAUTHORIZED: UnauthenticatedResponse,
            status.HTTP_404_NOT_FOUND: NotFoundResponse,
        }
    )
    @decorators.action(methods=["POST"], detail=True)
    def resend(self, request, pk):
        """
        Resend one received e-mail. The resend e-mail is an background task,
        then the return of that endpoint does not indicate that the
        e-mail is really delivered.
        """
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

    @swagger_auto_schema(
        responses={
            status.HTTP_401_UNAUTHORIZED: UnauthenticatedResponse,
        }
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieves an list of the received mails of the accounts
        that the authenticated user is the owner.
        """
        return super(UserReceivedMailViewSet, self).list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_401_UNAUTHORIZED: UnauthenticatedResponse,
            status.HTTP_404_NOT_FOUND: NotFoundResponse,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve one received mails of an account that the authenticated
        user is the owner by the received mail id.
        """
        return super(UserReceivedMailViewSet, self).retrieve(request, *args, **kwargs)

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

    @swagger_auto_schema(
        responses={
            status.HTTP_401_UNAUTHORIZED: UnauthenticatedResponse,
        },
    )
    def list(self, request, *args, **kwargs):
        """
        List the the accounts that the authenticated user is the
        owner.
        """
        return super(UserMailViewSet, self).list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_400_BAD_REQUEST: create_bad_request_response([
                "name",
                "mail_user",
                "redirect_enabled",
                "redirect_to",
            ]),
            status.HTTP_401_UNAUTHORIZED: UnauthenticatedResponse,
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Create an new mail account for the authenticated user
        (the authenticated user is the owner of the account).
        """
        return super(UserMailViewSet, self).create(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_401_UNAUTHORIZED: UnauthenticatedResponse,
            status.HTTP_404_NOT_FOUND: NotFoundResponse,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve one mail account that the authenticated user is owner
        by the account id.
        """
        return super(UserMailViewSet, self).retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_400_BAD_REQUEST: create_bad_request_response([
                "name",
                "mail_user",
                "redirect_enabled",
                "redirect_to",
            ]),
            status.HTTP_401_UNAUTHORIZED: UnauthenticatedResponse,
            status.HTTP_404_NOT_FOUND: NotFoundResponse,
        }
    )
    def update(self, request, *args, **kwargs):
        """
        Update one mail account that the authenticated user is owner
        by the account id.
        """
        return super(UserMailViewSet, self).update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_400_BAD_REQUEST: create_bad_request_response([
                "name",
                "mail_user",
                "redirect_enabled",
                "redirect_to",
            ]),
            status.HTTP_401_UNAUTHORIZED: UnauthenticatedResponse,
            status.HTTP_404_NOT_FOUND: NotFoundResponse,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partial update one mail account that the authenticated user is owner
        by the account id.
        """
        return super(UserMailViewSet, self).partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: "No body",
            status.HTTP_401_UNAUTHORIZED: UnauthenticatedResponse,
            status.HTTP_404_NOT_FOUND: NotFoundResponse,
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete one mail account that the authenticated user is owner by the
        account id.
        """
        return super(UserMailViewSet, self).destroy(request, *args, **kwargs)
