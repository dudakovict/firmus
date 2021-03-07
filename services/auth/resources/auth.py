from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from models import UserModel, RevokedTokenModel
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from twilio.base.exceptions import TwilioRestException
from marshmallow import ValidationError

from schemas import (
    UserRegisterSchema,
    UserCheckVerificationSchema,
    UserResendVerificationSchema,
    UserLoginSchema,
)

from errors import (
    UserEmailAlreadyExistsError,
    UserPhoneAlreadyExistsError,
    UserPhoneNotExistsError,
    UserEmailNotExistsError,
    UserNotVerifiedError,
    UserAlreadyVerifiedError,
    InvalidPhoneNumberError,
    InvalidVerificationCodeError,
    InvalidCredentialsError,
    InternalServerError,
)

user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()
user_check_verification_schema = UserCheckVerificationSchema()
user_resend_verification_schema = UserResendVerificationSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        try:
            user = user_register_schema.load(request.get_json())
            user.password = UserModel.generate_hash(user.password)
            user.send_verification_code()
            user.save_to_db()

            return user_register_schema.dump(user), 201
        except ValidationError:
            raise
        except (UserEmailAlreadyExistsError, UserPhoneAlreadyExistsError):
            raise
        except TwilioRestException:
            raise InvalidPhoneNumberError
        except:
            raise InternalServerError


class UserCheckVerification(Resource):
    @classmethod
    def post(cls):
        data = user_check_verification_schema.load(request.get_json())
        user = UserModel.find_by_phone(data.get("phone_number"))

        try:
            if user is None:
                raise NoResultFound
            if user.verified:
                raise InvalidRequestError
            if user.check_verification_code(data.get("code")):
                user.verified = True
                user.save_to_db()
                return user_check_verification_schema.dump(data)
            raise InvalidVerificationCodeError
        except NoResultFound:
            raise UserPhoneNotExistsError
        except InvalidRequestError:
            raise UserAlreadyVerifiedError
        except TwilioRestException:
            raise
        except InvalidVerificationCodeError:
            raise
        except:
            raise InternalServerError


class UserResendVerification(Resource):
    @classmethod
    def post(cls):
        data = user_resend_verification_schema.load(request.get_json())
        user = UserModel.find_by_phone(data.get("phone_number"))

        try:
            if user is None:
                raise NoResultFound
            if user.verified:
                raise InvalidRequestError
            user.send_verification_code()
            return user_resend_verification_schema.dump(data)
        except NoResultFound:
            raise UserPhoneNotExistsError
        except InvalidRequestError:
            raise UserAlreadyVerifiedError
        except TwilioRestException:
            raise
        except:
            raise InternalServerError


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user = user_login_schema.load(request.get_json())
        current_user = UserModel.find_by_email(user.email)

        try:
            if current_user is None:
                raise NoResultFound
            if not current_user.verified:
                raise UserNotVerifiedError
            if not UserModel.verify_hash(current_user.password, user.password):
                raise InvalidCredentialsError
            access_token = create_access_token(identity=current_user.id, fresh=True)
            refresh_token = create_refresh_token(identity=current_user.id)
            tokens = dict(
                [("access_token", access_token), ("refresh_token", refresh_token)]
            )
            return {"user": user_login_schema.dump(current_user), "tokens": tokens}, 200
        except NoResultFound:
            raise UserEmailNotExistsError
        except UserNotVerifiedError:
            raise
        except InvalidCredentialsError:
            raise
        except:
            raise InternalServerError


class UserLogoutAccess(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()["jti"]
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return None, 200
        except:
            raise InternalServerError


class UserLogoutRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        jti = get_jwt()["jti"]
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return None, 200
        except:
            raise InternalServerError


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {"access_token": access_token}, 200
