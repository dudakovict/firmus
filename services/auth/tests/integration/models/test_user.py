from models.user import UserModel, user_jobs
from models.category import CategoryModel
from models.job import JobModel
from tests.integration.integration_base_test import IntegrationBaseTest
from uuid import uuid4
from models.user import Gender
from datetime import date


class UserTest(IntegrationBaseTest):
    def setUp(self):
        super(UserTest, self).setUp()
        self.user = UserModel()
        self.user.id = uuid4().hex
        self.user.first_name = "test"
        self.user.last_name = "test"
        self.user.phone_number = "+3859999999"
        self.user.city = "test"
        self.user.birth_date = date(2021, 2, 20)
        self.user.gender = Gender("male")
        self.user.email = "test@gmail.com"
        self.user.password = "test"
        self.user.verified = False
        self.user.languages = ["HR", "EN"]
        self.user.availability = {
            "mon": True,
            "tue": False,
            "wed": True,
            "thu": False,
            "fri": True,
            "sat": False,
            "sun": True,
        }

    def test_crud(self):
        with self.app_context():
            self.assertIsNone(
                UserModel.find_by_email(self.user.email),
                f"Found a user with email {self.user.email} before persisting it to databse.",
            )

            self.user.save_to_db()

            self.assertIsNotNone(
                UserModel.find_by_email(self.user.email),
                f"Did not find a user with email {self.user.email} after persisting it to database.",
            )

            self.user.delete_from_db()

            self.assertIsNone(
                UserModel.find_by_email(self.user.email),
                f"Found a user with email {self.user.email} after deleting it from databse.",
            )

    def test_user_job_relationship(self):
        with self.app_context():
            CategoryModel("test").save_to_db()
            job = JobModel("test", "test")

            job.save_to_db()

            self.user.jobs.append(job)
            self.user.save_to_db()

            self.assertEqual(
                len(self.user.jobs), 1, f"Expected 1 but got {len(self.user.jobs)}."
            )
            self.assertEqual(
                job.users.count(), 1, f"Expected 1 but got {job.users.count()}."
            )
