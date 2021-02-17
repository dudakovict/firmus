from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)

from db import db
from models.user import UserModel, RevokedTokenModel
from schemas.user import UserSchema, UserVerificationSchema
from twilio.base.exceptions import TwilioRestException
from psycopg2.errors import UniqueViolation

user_schema = UserSchema()
user_verification_schema = UserVerificationSchema() 

AUTH_USER_CREATED = "User '{}' created."
AUTH_INTERNAL_SERVER_ERROR = "An unexpected error has occured."

VERIFY_USER_NOT_FOUND = "User with phone number '{}' doesn't exist."
VERIFY_USER_ALREADY_VERIFIED = "User with phone number '{}' has already been verified."
VERIFY_USER_VERIFIED = "User with phone number '{}' successfully verified."
VERIFY_USER_CODE_INCORRECT = "Incorrect verification code."
VERIFY_USER_CODE_RESENT = "Resent code to '{}'."
VERIFY_INTERNAL_SERVER_ERROR = "An unexpected error has occured."


class UserRegister(Resource):
    @classmethod
    def post(cls):
        try:
            user = user_schema.load(request.get_json())
            user.password = UserModel.generate_hash(user.password)
            user.save_to_db()
            verification = user.send_verification_code()
            return {
                "message": AUTH_USER_CREATED.format(user.email),
                "verification": verification,
            }, 200
        except UniqueViolation as exception:
            return {"message": exception}, 500
        except TwilioRestException as exception:
            user.delete_from_db()
            return {"message": exception.msg}, 500
        except:
            user.delete_from_db()
            return {"message": AUTH_INTERNAL_SERVER_ERROR}

class UserCheckVerification(Resource):
    @classmethod
    def post(cls):
        data = user_verification_schema.load(request.get_json())
        phone_number = data.get("phone_number")
        user = UserModel.find_by_phone(phone_number)
        if not user:
            return {"message": VERIFY_USER_NOT_FOUND.format(phone_number)}, 404
        if user.verified:
            return {"message": VERIFY_USER_ALREADY_VERIFIED.format(phone_number)}, 400
        try:
            verification_check = user.check_verification_code(data.get("code"))
            if verification_check.get("status") == "approved":
                user.verified = True
                user.save_to_db()
                return {"message": VERIFY_USER_VERIFIED.format(phone_number)}, 200
            return {"message": VERIFY_USER_CODE_INCORRECT}, 400
        except TwilioRestException as exception:
            return {"message": exception.msg}, 500
        except:
            return {"message": VERIFY_INTERNAL_SERVER_ERROR}, 500

class UserResendVerification(Resource):
    @classmethod
    def post(cls):
        data = user_verification_schema.load(request.get_json(), partial=("code",))
        phone_number = data.get("phone_number")
        user = UserModel.find_by_phone(phone_number)
        if not user:
            return {"message": VERIFY_USER_NOT_FOUND.format(phone_number)}, 404
        if user.verified:
            return {"message": VERIFY_USER_ALREADY_VERIFIED.format(phone_number)}, 400
        try:
            user.send_verification_code()
            return {"message": VERIFY_USER_CODE_RESENT.format(user.phone_number)}, 200
        except TwilioRestException as exception:
            return {"message": exception.msg}, 500
        except:
            return {"message": VERIFY_INTERNAL_SERVER_ERROR}, 500