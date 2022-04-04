from django.urls import path
from payments.views import MercadoPagoWebHook, test

urlpatterns = [
    path('webhook/', MercadoPagoWebHook.as_view()),
    path('test/', test),
]
