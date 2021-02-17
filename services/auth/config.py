import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=30)

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTRGES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DATABASE_URL = (
    f"postgres://{POSTGRES_USER}:{POSTRGES_PASSWORD}@postgres:5432/firmus"
)


class Config:
    SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_SECRET_KEY = SECRET_KEY
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES
    PROPAGATE_EXCEPTIONS = True
