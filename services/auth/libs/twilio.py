import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from typing import Dict

TWILIO_VERIFICATION_CODE_SENT = "Verification code successfully sent to '{}'"


class Twilio:
    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    SERVICE = os.environ.get("VERIFY_SERVICE_SID")
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    @classmethod
    def start_verification(cls, phone_number: str) -> Dict:
        try:
            verification = cls.client.verify.services(cls.SERVICE).verifications.create(
                to=phone_number, channel="sms"
            )

            return {
                "message": TWILIO_VERIFICATION_CODE_SENT.format(verification.to),
                "verification_sid": verification.sid,
            }, 201
        except TwilioRestException as exception:
            return {"message": exception.msg}, 400

    @classmethod
    def check_verification(cls, phone_number: str, code: str) -> Dict:
        try:
            verification_check = cls.client.verify.services(
                cls.SERVICE
            ).verification_checks.create(to=phone_number, code=code)

            return {"status": verification_check.status}
        except TwilioRestException as exception:
            return {"message": exception.msg}, 400
