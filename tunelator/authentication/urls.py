from django.urls import path
from authentication.views import (
    TokenObtainPairView,
    TokenRefreshView,
    UserCreateView,
    UserProfileDataView,
)

app_name = 'authentication'

urlpatterns = [
    path('create/', UserCreateView.as_view(), name="signup"),
    path('token/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('user/', UserProfileDataView.as_view(), name='user'),
]
