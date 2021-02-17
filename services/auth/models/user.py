from db import db
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from passlib.hash import pbkdf2_sha256 as sha256
from uuid import uuid4
from datetime import date
from enum import Enum
from libs.twilio import Twilio
from typing import Dict, List
from models.job import JobModel

user_jobs = db.Table(
    "user_jobs",
    db.Column("job_slug", db.String(20), db.ForeignKey(
        "jobs.slug"), primary_key=True),
    db.Column("user_id", db.String(50), db.ForeignKey(
        "users.id"), primary_key=True),
)


class Gender(Enum):
    male = 0
    female = 1
    other = 2


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(50), primary_key=True)
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
        "JobModel",
        cascade="all, delete",
        secondary=user_jobs,
        lazy="subquery",
        backref=db.backref(
            "users", cascade="all, delete", lazy="dynamic"),
    )

    def __init__(
        self,
        first_name: str,
        last_name: str,
        phone_number: str,
        city: str,
        birth_date: date,
        gender: Gender,
        email: str,
        password: str,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.id = uuid4().hex
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.city = city
        self.birth_date = birth_date
        self.gender = gender
        self.email = email
        self.password = password
        self.verified = False

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def send_verification_code(self) -> Dict:
        return Twilio.start_verification(self.phone_number)

    def check_verification_code(self, code: str) -> Dict:
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
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password: str, _hash: str) -> bool:
        return sha256.verify(password, _hash)


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
