""" destination-specific PII controls """

import json
import os
import boto3
from config import GUARDRAIL_ID, GUARDRAIL_VERSION

def for_partner(appointment: dict) -> dict:
    """ prepare appointment data for the third-party reminder provider """

    # Allow-list: explicitly include only fields the provider needs
    # to properly send a reminder to the user
    payload = {
        "appointment_id": appointment["appointment_id"],
        "phone": appointment["phone"],
        "appointment_date": appointment["appointment_date"],
    }

    # ApplyGuardrail is the decision check before outbound transfer.
    client = boto3.client("bedrock-runtime")

    response = client.apply_guardrail(
        guardrailIdentifier=GUARDRAIL_ID,
        guardrailVersion=GUARDRAIL_VERSION,
        source="OUTPUT",
        content=[
            {"text": {"text": json.dumps(payload)}}
        ],
    )

    if response["action"] != "NONE":
        raise ValueError(
            "Outbound payload blocked by the Bedrock Guardrail."
        )

    return payload


def _redact_text(text: str) -> str:
    """ detect PII and replace detected spans """
    if not text:
        return text

    client = boto3.client("comprehend")

    response = client.detect_pii_entities(
        Text=text,
        LanguageCode="en",
    )

    entities = sorted(
        response.get("Entities", []),
        key=lambda entity: entity["BeginOffset"],
        reverse=True,
    )

    for entity in entities:
        start = entity["BeginOffset"]
        end = entity["EndOffset"]
        text = text[:start] + "[REDACTED]" + text[end:]

    return text


def for_storage(value):
    """ return a PII-redacted copy before writing anything to storage """

    def sanitize(item):
        if isinstance(item, str):
            return _redact_text(item)

        if isinstance(item, dict):
            return {
                key: sanitize(val)
                for key, val in item.items()
            }

        if isinstance(item, list):
            return [sanitize(element) for element in item]

        return item

    return sanitize(value)