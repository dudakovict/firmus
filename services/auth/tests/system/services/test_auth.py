import json
from tests.system.system_base_test import SystemBaseTest
from models import UserModel, CategoryModel, JobModel
from errors import errors


class AuthTest(SystemBaseTest):
    def setUp(self):
        super(AuthTest, self).setUp()
        self.data = {
            "first_name": "test",
            "last_name": "test",
            "phone_number": "+385976370682",
            "city": "test",
            "birth_date": "2021-02-24",
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
            "jobs": [{"slug": "test"}],
        }

        self.user_job_list = ["test"]

    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/categories",
                    data=json.dumps({"name": "test"}),
                    headers={"Content-Type": "application/json"},
                )

                client.post(
                    "/auth/jobs",
                    data=json.dumps({"name": "test", "category_slug": "test"}),
                    headers={"Content-Type": "application/json"},
                )

                self.assertIsNotNone(
                    CategoryModel.find_by_slug("test"),
                    f"Did not find a category with slug 'test' after persisting it to database.",
                )

                self.assertIsNotNone(
                    JobModel.find_by_slug("test"),
                    f"Did not find a job with slug 'test' after persisting it to database.",
                )

                resp = client.post(
                    "/auth/register",
                    data=json.dumps(self.data),
                    headers={"Content-Type": "application/json"},
                )

                user = json.loads(resp.data)

                self.assertEqual(
                    resp.status_code, 201, f"Expected 201, but got {resp.status_code}."
                )

                self.assertEqual(
                    user.get("verified"),
                    False,
                    f"Expected {False}, but got {user.get('verified')}.",
                )

                self.assertListEqual(
                    user.get("jobs"),
                    self.data.get("jobs"),
                    f"Expected {self.data.get('jobs')}, but got {user.get('jobs')}.",
                )

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/categories",
                    data=json.dumps({"name": "test"}),
                    headers={"Content-Type": "application/json"},
                )

                client.post(
                    "/auth/jobs",
                    data=json.dumps({"name": "test", "category_slug": "test"}),
                    headers={"Content-Type": "application/json"},
                )

                self.assertIsNotNone(
                    CategoryModel.find_by_slug("test"),
                    f"Did not find a category with slug 'test' after persisting it to database.",
                )

                self.assertIsNotNone(
                    JobModel.find_by_slug("test"),
                    f"Did not find a job with slug 'test' after persisting it to database.",
                )

                client.post(
                    "/auth/register",
                    data=json.dumps(self.data),
                    headers={"Content-Type": "application/json"},
                )

                resp = client.post(
                    "/auth/register",
                    data=json.dumps(self.data),
                    headers={"Content-Type": "application/json"},
                )

                self.assertEqual(
                    resp.status_code, 400, f"Expected 400, but got {resp.status_code}."
                )

                self.assertDictEqual(
                    errors.get("UserEmailAlreadyExistsError"),
                    json.loads(resp.data),
                    f"Expected {errors.get('UserEmailAlreadyExistsError')}, but got {json.loads(resp.data)}.",
                )

    def test_login_user_not_verified(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/categories",
                    data=json.dumps({"name": "test"}),
                    headers={"Content-Type": "application/json"},
                )

                client.post(
                    "/auth/jobs",
                    data=json.dumps({"name": "test", "category_slug": "test"}),
                    headers={"Content-Type": "application/json"},
                )

                client.post(
                    "/auth/register",
                    data=json.dumps(self.data),
                    headers={"Content-Type": "application/json"},
                )

                resp = client.post(
                    "/auth/login",
                    data=json.dumps({"email": "test@gmail.com", "password": "test"}),
                    headers={"Content-Type": "application/json"},
                )

                self.assertEqual(
                    resp.status_code, 400, f"Expected 400, but got {resp.status_code}."
                )

                self.assertDictEqual(
                    errors.get("UserNotVerifiedError"),
                    json.loads(resp.data),
                    f"Expected {errors.get('UserNotVerifiedError')}, but got {json.loads(resp.data)}.",
                )

    def test_login_user_verified(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/categories",
                    data=json.dumps({"name": "test"}),
                    headers={"Content-Type": "application/json"},
                )

                client.post(
                    "/auth/jobs",
                    data=json.dumps({"name": "test", "category_slug": "test"}),
                    headers={"Content-Type": "application/json"},
                )

                client.post(
                    "/auth/register",
                    data=json.dumps(self.data),
                    headers={"Content-Type": "application/json"},
                )

                user = UserModel.find_by_email("test@gmail.com")
                user.verified = True
                user.save_to_db()

                resp = client.post(
                    "/auth/login",
                    data=json.dumps({"email": "test@gmail.com", "password": "test"}),
                    headers={"Content-Type": "application/json"},
                )

                self.assertEqual(
                    resp.status_code, 200, f"Expected 200, but got {resp.status_code}."
                )

                login_resp = json.loads(resp.data)

                self.assertListEqual(
                    self.user_job_list,
                    login_resp.get("user").get("jobs"),
                    f"Expected {self.user_job_list}, but got {login_resp.get('user').get('jobs')}.",
                )

                self.assertIsNotNone(
                    login_resp.get("tokens").get("access_token"),
                    f"Expected a JWT access token, but got {login_resp.get('tokens').get('access_token')}.",
                )

                self.assertIsNotNone(
                    login_resp.get("tokens").get("refresh_token"),
                    f"Expected a JWT refresh token, but got {login_resp.get('tokens').get('refresh_token')}.",
                )
