from rest_framework import mixins, viewsets
from content.serializers import SocialContentSerializer
from content.models import SocialContent

class SocialContentViewSet(mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    Social content viewset
    """
    serializer_class = SocialContentSerializer
    queryset = SocialContent.objects.order_by('updated_at').all()
