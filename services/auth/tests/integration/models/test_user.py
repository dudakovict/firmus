from tests.integration.integration_base_test import IntegrationBaseTest
from models import UserModel


class UserTest(IntegrationBaseTest):
    def setUp(self):
        super(UserTest, self).setUp()
        self.user_data = {
            "first_name": "test",
            "last_name": "test",
            "phone_number": "+385999999999",
            "city": "test",
            "birth_date": "2021-02-20",
            "gender": "male",
            "email": "test@gmail.com",
            "password": "test",
            "languages": ["HR", "EN"],
            "availability": {
                "mon": True,
                "tue": False,
                "wed": True,
                "thu": False,
                "fri": True,
                "sat": False,
                "sun": True,
            },
            "jobs": [],
        }

        self.category_data = {"name": "test"}

        self.job_data = {"name": "test", "category_slug": "test"}

    def test_crud(self):
        with self.app_context():
            user = self.user_schema.load(self.user_data)
            self.assertIsNone(
                UserModel.find_by_email(user.email),
                f"Found a user with email {user.email} before persisting it to databse.",
            )

            user.save_to_db()

            self.assertIsNotNone(
                UserModel.find_by_email(user.email),
                f"Did not find a user with email {user.email} after persisting it to database.",
            )

            user.delete_from_db()

            self.assertIsNone(
                UserModel.find_by_email(user.email),
                f"Found a user with email {user.email} after deleting it from databse.",
            )

    def test_user_job_relationship(self):
        with self.app_context():
            self.category_schema.load(self.category_data).save_to_db()

            job = self.job_schema.load(self.job_data)

            job.save_to_db()

            user = self.user_schema.load(self.user_data)

            user.jobs.append(job)
            user.save_to_db()

            self.assertEqual(
                user.jobs.all()[0].name,
                job.name,
                f"Expected {job.name} but got {user.jobs.all()[0].name}.",
            )

            self.assertEqual(
                user.jobs.count(), 1, f"Expected 1 but got {user.jobs.count()}."
            )

            self.assertEqual(
                job.users.count(), 1, f"Expected 1 but got {job.users.count()}."
            )
