from drf_spectacular.utils import extend_schema_field
from psycopg.types.range import DateRange
from rest_framework import serializers


@extend_schema_field(
    {
        "type": "object",
        "required": ["beginGeldigheid"],
        "properties": {
            "beginGeldigheid": {"type": "string", "format": "date"},
            "eindeGeldigheid": {
                "type": "string",
                "format": "date",
                "nullable": True,
            },
        },
        "example": {
            "beginGeldigheid": "2025-01-01",
            "eindeGeldigheid": "2025-06-01",
        },
    }
)
class PeriodField(serializers.Field):
    def to_representation(self, value):
        return {
            "begin_geldigheid": value.lower,
            "einde_geldigheid": value.upper,
        }

    def to_internal_value(self, data):
        start = data.get("begin_geldigheid")
        end = data.get("einde_geldigheid")

        if not start:
            raise serializers.ValidationError(
                {"begin_geldigheid": "Begin geldigheid is verplicht."}
            )

        start = serializers.DateField().to_internal_value(start)

        if end is not None:
            end = serializers.DateField().to_internal_value(end)

        if end and start > end:
            raise serializers.ValidationError(
                "Einde geldigheid moet na begin geldigheid liggen."
            )

        return DateRange(start, end)


@extend_schema_field(
    {
        "type": "array",
        "items": {
            "type": "object",
            "required": ["beginGeldigheid"],
            "properties": {
                "beginGeldigheid": {"type": "string", "format": "date"},
                "eindeGeldigheid": {
                    "type": "string",
                    "format": "date",
                    "nullable": True,
                },
            },
        },
        "example": [
            {
                "beginGeldigheid": "2025-01-01",
                "eindeGeldigheid": "2025-06-01",
            }
        ],
    }
)
class PeriodListField(serializers.Field):
    def to_representation(self, value):
        if value is None:
            return []

        return [
            {
                "begin_geldigheid": v.lower,
                "einde_geldigheid": v.upper,
            }
            for v in value
        ]

    def to_internal_value(self, data):
        raise NotImplementedError("Dit veld is read-only.")
