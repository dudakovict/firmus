from unittest import TestCase
from app import app
from db import db


class IntegrationBaseTest(TestCase):
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

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
