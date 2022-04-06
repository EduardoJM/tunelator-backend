from django.urls import path, include
from authentication.views import (
    TokenObtainPairView,
    TokenRefreshView,
    UserCreateSerializer,
)

urlpatterns = [
    path('create/', UserCreateSerializer.as_view(), name="new_user"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
