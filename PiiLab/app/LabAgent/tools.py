# fake clinic backing store
FAKE_APPOINTMENTS={
    "APT-104": {
        "appointment_id": "APT-104",
        "patient_name": "Jamie Example",
        "email": "jamie@example.com",
        "phone": "555-010-0199",
        "appointment_date": "2026-10-08",
        "appointment_type": "Dental cleaning",
        "notes": "Patient requested a morning appointment. Legacy payment reference copied into notes by mistake: 4111111111111111. Please do not use this reference."
    },
    "APT-105": {
        "appointment_id": "APT-105",
        "patient_name": "Taylor Sample",
        "email": "taylor@example.com",
        "phone": "555-010-0128",
        "appointment_date": "2026-10-09",
        "appointment_type": "Routine checkup",
        "notes": "Prefers appointment reminders by phone."
    },
    "APT-106": {
        "appointment_id": "APT-106",
        "patient_name": "Morgan Demo",
        "email": "morgan@example.com",
        "phone": "555-010-0164",
        "appointment_date": "2026-10-12",
        "appointment_type": "Eye exam",
        "notes": "Requested an appointment after 2 PM."
    }
}

from controls import for_partner
from store import save_record

def get_appointment(appointment_id: str) -> dict:
    """get an appointment by its id"""

    record = FAKE_APPOINTMENTS.get(appointment_id)

    if record is None:
        return {"error": "Appointment not found"}

    appointment = dict(record)
    save_record(appointment)

    return appointment

def send_appointment_reminder(appointment_id : str) -> dict:
    """ simulate a third-party appointment reminder service """

    record = get_appointment(appointment_id)

    if "error" in record:
        return {
            "status": "not-accepted",
            "provider": "FakeReminderService",
            "received_payload": "Not found"
        }

    safe_payload = for_partner(record)

    return {
        "status": "accepted",
        "provider": "FakeReminderService",
        "received_payload": safe_payload,
    }