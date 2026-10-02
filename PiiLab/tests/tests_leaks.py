
import json

from ..app.LabAgent.controls import for_storage
from ..app.LabAgent import controls

# third part pii test
def test_outbound_payload_contains_only_approved_fields(monkeypatch):
    """The reminder provider should receive only approved fields."""

    captured = {}

    class FakeBedrockClient:
        def apply_guardrail(self, **kwargs):
            captured.update(kwargs)
            return {"action": "NONE"}

    monkeypatch.setattr(
        controls.boto3,
        "client",
        lambda service: FakeBedrockClient(),
    )

    appointment = {
        "appointment_id": "APT-104",
        "name": "Jamie Example",
        "email": "jamie@example.com",
        "phone": "555-010-0199",
        "appointment_date": "2026-10-08",
        "notes": "Private notes and 4111111111111111",
    }

    result = controls.for_partner(appointment)

    assert set(result.keys()) == {
        "appointment_id",
        "phone",
        "appointment_date",
    }
    assert "name" not in result
    assert "email" not in result
    assert "notes" not in result

    checked_payload = json.loads(
        captured["content"][0]["text"]["text"]
    )
    assert checked_payload == result

# storage pii test
def test_storage_redacts_pii():
    """PII should be redacted before a record is persisted."""

    appointment = {
        "appointment_id": "APT-104",
        "name": "Jamie Example",
        "email": "jamie@example.com",
        "notes": "Contact Jamie Example at jamie@example.com",
    }

    redacted = for_storage(appointment)

    serialized = json.dumps(redacted)

    assert "Jamie Example" not in serialized
    assert "jamie@example.com" not in serialized
    assert "[REDACTED]" in serialized