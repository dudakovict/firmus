from libs import client, service


class Twilio:
    @classmethod
    def start_verification(cls, phone_number: str) -> None:
        client.verify.services(service).verifications.create(
            to=phone_number, channel="sms"
        )

    @classmethod
    def check_verification(cls, phone_number: str, code: str) -> bool:
        verification_check = client.verify.services(service).verification_checks.create(
            to=phone_number, code=code
        )

        return verification_check.status == "approved"
