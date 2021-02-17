from ma import ma
from marshmallow import Schema, fields
from db import db
from models.user import UserModel
from schemas.job import UserJobSchema
from marshmallow import pre_load
from psycopg2.errors import UniqueViolation

USER_EMAIL_ALREADY_EXISTS = "User with email '{}' already exists."
USER_PHONE_NUMBER_ALREADY_EXISTS = "User with phone number '{}' already exists."

class UserSchema(ma.SQLAlchemyAutoSchema):
    jobs = ma.Nested(UserJobSchema, many=True, only=["slug"])

    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        load_instance = True
        sqla_session = db.session

    @pre_load
    def check_email_and_phone_number(self, in_data, **kwargs):
        email = in_data.get("email")
        phone_number = in_data.get("phone_number")
        if UserModel.find_by_email(email):
            raise UniqueViolation(USER_EMAIL_ALREADY_EXISTS.format(email))  
        if UserModel.find_by_phone(phone_number):
            raise UniqueViolation(USER_PHONE_NUMBER_ALREADY_EXISTS.format(phone_number))
        return in_data

class UserVerificationSchema(Schema):
    phone_number = fields.Str(required=True)
    code = fields.Str(required=True)