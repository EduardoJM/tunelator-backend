from django.urls import path
from authentication.views import (
    TokenObtainPairView,
    TokenRefreshView,
    UserCreateView,
)

urlpatterns = [
    path('create/', UserCreateView.as_view(), name="new_user"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
