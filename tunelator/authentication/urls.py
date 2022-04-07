from django.urls import path
from authentication.views import (
    TokenObtainPairView,
    TokenRefreshView,
    UserCreateView,
    UserFCMTokenReceiveView,
)

urlpatterns = [
    path('create/', UserCreateView.as_view(), name="new_user"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/fcm/', UserFCMTokenReceiveView.as_view(), name='firebase_cloud_messaging_token')
]
