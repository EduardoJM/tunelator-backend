from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, status
from drf_yasg.utils import swagger_auto_schema
from content.serializers import SocialContentSerializer
from content.models import SocialContent
from docs.responses import UnauthenticatedResponse

class SocialContentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SocialContentSerializer
    queryset = SocialContent.objects.order_by('-updated_at').all()
    filter_backends = [DjangoFilterBackend]

    @swagger_auto_schema(
        responses={
            status.HTTP_401_UNAUTHORIZED: UnauthenticatedResponse
        }
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieves an list of social network contents registered in the
        admin painel about the Tunelator, privacity and related contents.
        
        Must be used to create cards like an blog shortcut.
        """
        return super(SocialContentViewSet, self).list(request, *args, **kwargs)
