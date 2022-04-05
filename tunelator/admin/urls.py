from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('', admin.site.urls)
]
