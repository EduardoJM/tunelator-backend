from django.urls import path, include
from rest_framework import routers
from mails.viewsets import UserMailViewSet, UserReceivedMailViewSet
from mails.views import VerifyUserSystemAPIView

mails_router = routers.SimpleRouter()
mails_router.register("", UserMailViewSet, basename="UserMail")
mails_router.register("received", UserReceivedMailViewSet, basename="UserReceivedMail")

urlpatterns = [
    path('', include(mails_router.urls)),
    path('verify/user/', VerifyUserSystemAPIView.as_view()),
]
