import os
from datetime import timedelta
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=30)

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTRGES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DATABASE_URL = f"postgres://{POSTGRES_USER}:{POSTRGES_PASSWORD}@localhost:5432/firmus"


class BaseConfig:
    API_PREFIX = "/auth"
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    VERIFY_SERVICE_SID = os.environ.get("VERIFY_SERVICE_SID")


class DevelopmentConfig(BaseConfig):
    FLASK_ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DATABASE_URL


class ProductionConfig(BaseConfig):
    FLASK_ENV = "production"
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_DATABASE_URI = DATABASE_URL


class TestConfig(BaseConfig):
    FLASK_ENV = "development"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
