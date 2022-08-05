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
