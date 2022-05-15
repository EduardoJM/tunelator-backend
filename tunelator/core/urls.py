from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('api/plans/', include('plans.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/mails/', include('mails.urls')),
    path('docs/', include('docs.urls')),
]
