import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from mails.serializers import UserMailVerifySerializer

class VerifyUserSystemAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = UserMailVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_name = serializer.validated_data["user_name"]
        url = "%s/verify/" % settings.USER_SYSTEM_URL
        headers = {
            'Authorization': 'Bearer %s' % settings.USER_SYSTEM_AUTHORIZATION
        }
        payload = {
            "user_name": user_name,
        }
        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            return Response({ 'detail': 'Nome de e-mail não disponível.' }, status=status.HTTP_400_BAD_REQUEST)
        return Response({ 'detail': 'Nome de e-mail disponível' }, status=status.HTTP_200_OK)
