from django.urls import path
from content.viewsets import SocialContentViewset

app_name = 'content'

urlpatterns = [
    path('', SocialContentViewset.as_view(), name="social_contents"),
]

