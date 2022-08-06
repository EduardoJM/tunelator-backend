from typing import List
from drf_yasg import openapi

NotFoundResponse = openapi.Response(
    "Not found.",
    openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(
                "error message",
                "Localizated (i18n) error message",
                openapi.TYPE_STRING,
                example="Not Found."
            ),
        },
    ),
)

UnauthenticatedResponse = openapi.Response(
    "Unauthenticated.",
    openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(
                "error message",
                "Localizated (i18n) error message",
                openapi.TYPE_STRING,
                example="Authentication credentials not found."
            ),
        },
    ),
)

WrongCredentialsResponse = openapi.Response(
    "Unauthenticated.",
    openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(
                "error message",
                "Localizated (i18n) error message",
                openapi.TYPE_STRING,
                example="Email or password is incorrect."
            ),
        },
    ),
)

InvalidTokenResponse = openapi.Response(
    "Unauthenticated.",
    openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(
                "error message",
                "Localizated (i18n) error message",
                openapi.TYPE_STRING,
                example="The token is expired or invalid."
            ),
        },
    ),
)

def create_bad_request_response(fields: List[str]):
    properties = {}
    for field in fields:
        properties[field] = openapi.Schema(
            "field error messages",
            "Localizated (i18n) validation error messages",
            openapi.TYPE_ARRAY,
            items=openapi.Schema(
                "error message",
                "Localizated (i18n) error message",
                openapi.TYPE_STRING,
                example="Invalid field value description."
            )
        )

    return openapi.Response(
        "Bad Request.",
        openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=properties
        ),
    )
