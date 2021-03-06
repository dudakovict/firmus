import json
from unittest import TestCase
from run import app
from models import db


class SystemBaseTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
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
