from drf_yasg import openapi

IndisponibleResponse = openapi.Response(
    "Indisponible.",
    openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(
                "error message",
                "Localizated (i18n) error message",
                openapi.TYPE_STRING,
                example="Mail username is indisponible."
            ),
        },
    ),
)

DisponibleResponse = openapi.Response(
    "Disponible.",
    openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(
                "error message",
                "Localizated (i18n) error message",
                openapi.TYPE_STRING,
                example="Mail username is disponible."
            ),
        },
    ),
)
