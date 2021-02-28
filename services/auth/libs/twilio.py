import os
from twilio.rest import Client


class Twilio:
    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    SERVICE = os.environ.get("VERIFY_SERVICE_SID")
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    @classmethod
    def start_verification(cls, phone_number: str) -> None:
        cls.client.verify.services(cls.SERVICE).verifications.create(
            to=phone_number, channel="sms"
        )

    @classmethod
    def check_verification(cls, phone_number: str, code: str) -> bool:
        verification_check = cls.client.verify.services(
            cls.SERVICE
        ).verification_checks.create(to=phone_number, code=code)

        return verification_check.status == "approved"
