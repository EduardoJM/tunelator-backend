from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException

class UnprocessableEntity(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = _('The entity is unprocessable.')
    default_code = 'unprocessable_entity'

class EmailUsernameAlreadyUsed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('E-mail username is already used.')
    default_code = 'username_already_used'

class ReceivedMailNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Received mail not found.')
    default_code = 'received_mail_not_found'
