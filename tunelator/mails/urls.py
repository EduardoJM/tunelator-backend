from django.urls import path, include
from rest_framework import routers
from mails.viewsets import UserMailViewSet

mails_router = routers.SimpleRouter()
mails_router.register("", UserMailViewSet, basename="UserMail")

urlpatterns = [
    path('', include(mails_router.urls)),
]
