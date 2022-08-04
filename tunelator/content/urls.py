from django.urls import path, include
from rest_framework import routers
from content.viewsets import SocialContentViewSet

content_router = routers.SimpleRouter()
content_router.register("", SocialContentViewSet, basename="SocialContent")

app_name = 'content'

urlpatterns = [
    path('', include(content_router.urls)),
]
