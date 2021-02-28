import json
from unittest import TestCase
from app import app
from db import db
from models.user import UserModel, user_jobs
from models.category import CategoryModel
from models.job import JobModel


class SystemBaseTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "postgresql://postgres:firmuspostgres@localhost:5432/firmus_test"
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        with app.app_context():
            db.create_all()
        self.app = app.test_client
        self.app_context = app.app_context
        self.app().post(
            "/categories",
            data=json.dumps({"name": "test"}),
            headers={"Content-Type": "application/json"},
        )
        self.app().post(
            "/jobs",
            data=json.dumps({"name": "test", "category_slug": "test"}),
            headers={"Content-Type": "application/json"},
        )

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
