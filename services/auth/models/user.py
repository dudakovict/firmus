from models import bcrypt, db
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON
from uuid import uuid4
from datetime import date
from enum import Enum
from libs import Twilio
from typing import List

user_jobs = db.Table(
    "user_jobs",
    db.Column("job_slug", db.String(20), db.ForeignKey("jobs.slug"), primary_key=True),
    db.Column(
        "user_id", UUID(as_uuid=True), db.ForeignKey("users.id"), primary_key=True
    ),
)


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid4().hex)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(155), nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(155), nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    languages = db.Column(ARRAY(db.String(2)), nullable=False)
    availability = db.Column(JSON, nullable=False)
    jobs = db.relationship(
        "JobModel", secondary=user_jobs, lazy="dynamic", back_populates="users"
    )

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def send_verification_code(self) -> None:
        Twilio.start_verification(self.phone_number)

    def check_verification_code(self, code: str) -> bool:
        return Twilio.check_verification(self.phone_number, code)

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_phone(cls, phone_number: str) -> "UserModel":
        return cls.query.filter_by(phone_number=phone_number).first()

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    @staticmethod
    def generate_hash(password: str) -> str:
        return bcrypt.generate_password_hash(password).decode("utf8")

    @staticmethod
    def verify_hash(pw_hash: str, password: str) -> bool:
        return bcrypt.check_password_hash(pw_hash, password)


class RevokedTokenModel(db.Model):
    __tablename__ = "revoked_tokens"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), nullable=False)

    def add(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti: str) -> bool:
        return bool(cls.query.filter_by(jti=jti).first())
