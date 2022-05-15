from django.views.generic import TemplateView
from django.urls import path
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('openapi/', get_schema_view(
        title="Tunelator",
        description="Api for the tunelator project",
        authentication_classes=[],
        permission_classes=[]
    ), name='openapi-schema'),
    path('redoc/', TemplateView.as_view(template_name='redoc.html', extra_context={'schema_url':'openapi-schema'}), name='redoc'),
]
