from django.conf import settings
import requests

def validate_user_name(user_name: str) -> bool:
    url = "%s/verify/" % settings.USER_SYSTEM_URL
    headers = {
        'Authorization': 'Bearer %s' % settings.USER_SYSTEM_AUTHORIZATION
    }
    payload = {
        "user_name": str(user_name).lower(),
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code == 200
