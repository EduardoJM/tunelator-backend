from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        path('admin/', admin.site.urls)
    ]

urlpatterns += [
    path('auth/', include('authentication.urls')),
    path('api/plans/', include('plans.urls')),
    path('api/payments/', include('payments.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
