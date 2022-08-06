from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from mails.serializers import UserMailVerifySerializer
from mails.services import validate_user_name
from mails.schemas import IndisponibleResponse, DisponibleResponse

class VerifyUserSystemAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=UserMailVerifySerializer,
        responses={
            status.HTTP_400_BAD_REQUEST: IndisponibleResponse,
            status.HTTP_200_OK: DisponibleResponse,
        },
    )
    def post(self, request):
        """
        Proxy for the user system API verify if an username is
        disponible or no.
        """
        serializer = UserMailVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_name = serializer.validated_data["user_name"]
        if not validate_user_name(user_name):
            return Response({ 'detail': 'Nome de e-mail não disponível.' }, status=status.HTTP_400_BAD_REQUEST)
        return Response({ 'detail': 'Nome de e-mail disponível' }, status=status.HTTP_200_OK)
