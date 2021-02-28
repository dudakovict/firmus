from db import db
from ma import ma
from marshmallow import Schema, fields, pre_load, post_dump
from models.user import UserModel
from schemas.job import UserJobSchema
from errors import UserEmailAlreadyExistsError, UserPhoneAlreadyExistsError


class UserRegisterSchema(ma.SQLAlchemyAutoSchema):
    jobs = ma.Nested(UserJobSchema, many=True, only=("slug",), required=True)

    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "verified")
        include_fk = True
        load_instance = True
        sqla_session = db.session

    @pre_load
    def check_email_and_phone_number(self, data, **kwargs):
        email = data.get("email")
        phone_number = data.get("phone_number")
        if UserModel.find_by_email(email):
            raise UserEmailAlreadyExistsError
        if UserModel.find_by_phone(phone_number):
            raise UserPhoneAlreadyExistsError
        return data


class UserCheckVerificationSchema(Schema):
    phone_number = fields.Str(required=True)
    code = fields.Str(required=True)

    @post_dump
    def verification_success(self, data, **kwargs):
        phone_number = data.get("phone_number")
        return {
            "message": f"User with phone number '{phone_number}' successfully verified.",
            "status": 200,
        }


class UserResendVerificationSchema(Schema):
    phone_number = fields.Str(required=True)

    @post_dump
    def resend_verification_sucess(self, data, **kwargs):
        phone_number = data.get("phone_number")
        return {
            "message": f"Resent verification code to '{phone_number}.",
            "status": 200,
        }


class UserLoginSchema(ma.SQLAlchemyAutoSchema):
    jobs = ma.Nested(UserJobSchema, many=True, only=("slug",))

    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = (
            "id",
            "verified",
            "first_name",
            "last_name",
            "phone_number",
            "city",
            "birth_date",
            "gender",
            "languages",
            "availability",
            "jobs",
        )
        include_fk = True
        load_instance = True
        sqla_session = db.session

    @post_dump
    def login_success(self, data, **kwargs):
        [data.pop(key) for key in ["verified", "created_at", "updated_at"]]
        data["jobs"] = [job["slug"] for job in data.get("jobs")]
        return data
