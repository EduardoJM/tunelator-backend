from django.urls import path
from authentication.views import (
    TokenObtainPairView,
    TokenRefreshView,
    UserCreateView,
    UserProfileDataView,
    ForgotPasswordSessionView,
    ForgotPasswordValidateSessionView,
    ForgotPasswordSessionResetView,
)

app_name = 'authentication'

urlpatterns = [
    path('create/', UserCreateView.as_view(), name="signup"),
    path('token/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('user/', UserProfileDataView.as_view(), name='user'),
    path('recovery/', ForgotPasswordSessionView.as_view(), name='recovery'),
    path(
        'recovery/<session_id>/',
        ForgotPasswordValidateSessionView.as_view(),
        name='recovery-validate'
    ),
    path(
        'recovery/<session_id>/reset/',
        ForgotPasswordSessionResetView.as_view(),
        name='recovery-reset'
    ),
]
