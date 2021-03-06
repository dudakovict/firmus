from unittest import TestCase
from run import app
from models import db
from schemas import CategorySchema, JobSchema, UserRegisterSchema


class IntegrationBaseTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        with app.app_context():
            db.create_all()
        self.app = app.test_client
        self.app_context = app.app_context
        self.category_schema = CategorySchema()
        self.job_schema = JobSchema()
        self.user_schema = UserRegisterSchema()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
