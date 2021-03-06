import json
from models.job import JobModel
from models.category import CategoryModel
from tests.system.system_base_test import SystemBaseTest
from errors import errors


class JobTest(SystemBaseTest):
    def setUp(self):
        super(JobTest, self).setUp()

        self.expected_job = {"name": "test", "slug": "test", "category_slug": "test"}

        self.expected_job_list = {
            "jobs": [{"name": "test", "slug": "test", "category_slug": "test"}]
        }

    def test_create_job(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/auth/categories",
                    data=json.dumps({"name": "test"}),
                    headers={"Content-Type": "application/json"},
                )

                resp = client.post(
                    "/auth/jobs",
                    data=json.dumps({"name": "test", "category_slug": "test"}),
                    headers={"Content-Type": "application/json"},
                )

                self.assertEqual(
                    resp.status_code, 201, f"Expected 201, but got {resp.status_code}."
                )

                self.assertIsNotNone(
                    JobModel.find_by_slug("test"),
                    f"Did not find a job with slug {self.expected_job.get('slug')} after persisting it to database.",
                )

                self.assertDictEqual(
                    self.expected_job,
                    json.loads(resp.data),
                    f"Expected {self.expected_job}, but got {json.loads(resp.data)}.",
                )

    def test_create_duplicate_job(self):
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

                resp = client.post(
                    "/auth/jobs",
                    data=json.dumps({"name": "test", "category_slug": "test"}),
                    headers={"Content-Type": "application/json"},
                )

                self.assertEqual(
                    resp.status_code, 400, f"Expected 400, but got {resp.status_code}."
                )

                self.assertDictEqual(
                    errors.get("JobAlreadyExistsError"),
                    json.loads(resp.data),
                    f"Expected {errors.get('JobAlreadyExistsError')}, but got {json.loads(resp.data)}.",
                )

    def test_delete_job(self):
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
                    JobModel.find_by_slug("test"),
                    f"Did not find a job with slug {self.expected_job.get('slug')} after persisting it to database.",
                )

                resp = client.delete("/auth/jobs/test")

                self.assertEqual(
                    resp.status_code, 204, f"Expected 204, but got {resp.status_code}."
                )

                self.assertIsNone(
                    JobModel.find_by_slug("test"),
                    f"Found a job with slug {self.expected_job.get('slug')} after deleting it from database.",
                )

                self.assertEqual(
                    b"", resp.data, f"Expected no content, but got {resp.data}."
                )

    def test_find_job(self):
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

                resp = client.get("/auth/jobs/test")

                self.assertEqual(
                    resp.status_code, 200, f"Expected 200, but got {resp.status_code}."
                )

                self.assertDictEqual(
                    self.expected_job,
                    json.loads(resp.data),
                    f"Expected {self.expected_job}, but got {json.loads(resp.data)}.",
                )

    def test_job_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get("/auth/jobs/test")

                self.assertEqual(
                    resp.status_code, 404, f"Expected 404, but got {resp.status_code}."
                )

                self.assertDictEqual(
                    errors.get("JobNotExistsError"),
                    json.loads(resp.data),
                    f"Expected {errors.get('JobNotExistsError')}, but got {json.loads(resp.data)}.",
                )

    def test_list_job(self):
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

                resp = client.get("/auth/jobs")

                self.assertEqual(
                    resp.status_code, 200, f"Expected 200, but got {resp.status_code}."
                )

                self.assertDictEqual(
                    self.expected_job_list,
                    json.loads(resp.data),
                    f"Expected {self.expected_job_list}, but got {json.loads(resp.data)}.",
                )
