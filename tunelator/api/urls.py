from django.urls import path, include

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('plans/', include('plans.urls')),
    path('payments/', include('payments.urls')),
    path('mails/', include('mails.urls')),
    path('content/', include('content.urls')),
]