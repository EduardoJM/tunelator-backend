from django.urls import path, include
from rest_framework import routers
from plans.viewsets import PlanViewSet

plans_router = routers.SimpleRouter()
plans_router.register("", PlanViewSet, basename="Plan")

app_name = 'plans'

urlpatterns = [
    path('', include(plans_router.urls)),
]
