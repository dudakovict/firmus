import json, sys
from models import CategoryModel
from models.job import JobModel
from tests.system.system_base_test import SystemBaseTest
from errors import errors


class CategoryTest(SystemBaseTest):
    
    def setUp(self):
        super(CategoryTest, self).setUp()

        self.expected_category = {"name": "test", "slug": "test", "jobs": []}

        self.expected_category_with_jobs = {
            "name": "test",
            "slug": "test",
            "jobs": [{"name": "test", "slug": "test", "category_slug": "test"}],
        }

        self.expected_category_list = {
            "categories": [{"name": "test", "slug": "test", "jobs": []}]
        }

        self.expected_category_list_with_jobs = {
            "categories": [
                {
                    "name": "test",
                    "slug": "test",
                    "jobs": [
                        {
                            "name": "test",
                            "slug": "test",
                            "category_slug": "test",
                        }
                    ],
                }
            ]
        }
    
    def test_create_category(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post('/auth/categories', data=json.dumps({"name": "test"}), headers={"Content-Type": "application/json"})
                self.assertEqual(resp.status_code, 201, f"Expected 201, but got {resp.status_code}.")
                self.assertIsNotNone(CategoryModel.find_by_slug("test"), f"Did not find a category with slug {self.expected_category.get('slug')} after persisting it to database.")
                self.assertDictEqual(self.expected_category, json.loads(resp.data), f"Expected {self.expected_category}, but got {json.loads(resp.data)}.")
    
    
    def test_create_duplicate_category(self):
        with self.app() as client:
            with self.app_context():
                client.post('/auth/categories', data=json.dumps({"name": "test"}), headers={"Content-Type": "application/json"})
                resp = client.post('/auth/categories', data=json.dumps({"name": "test"}), headers={"Content-Type": "application/json"})
                self.assertEqual(resp.status_code, 400, f"Expected 400, but got {resp.status_code}.")
                self.assertDictEqual(
                    errors.get("CategoryAlreadyExistsError"),
                    json.loads(resp.data),
                    f"Expected {errors.get('CategoryAlreadyExistsError')}, but got {json.loads(resp.data)}.",
                )

    
    def test_delete_category(self):
        with self.app() as client:
            with self.app_context():
                client.post('/auth/categories', data=json.dumps({"name": "test"}), headers={"Content-Type": "application/json"})

                self.assertIsNotNone(
                    CategoryModel.find_by_slug("test"),
                    f"Did not find a category with slug {self.expected_category.get('slug')} after persisting it to database.",
                )

                resp = client.delete("/auth/categories/test")

                self.assertEqual(
                    resp.status_code, 204, f"Expected 204, but got {resp.status_code}."
                )

                self.assertIsNone(
                    CategoryModel.find_by_slug("test"),
                    f"Found a category with slug {self.expected_category.get('slug')} after deleting it from database.",
                )
    	        
                self.assertEqual(
                    b"", resp.data, f"Expected no content, but got {resp.data}."
                )
    
    def test_find_category(self):
        with self.app() as client:
            with self.app_context():
                client.post('/auth/categories', data=json.dumps({"name": "test"}), headers={"Content-Type": "application/json"})

                resp = client.get("/auth/categories/test")

                self.assertEqual(
                    resp.status_code, 200, f"Expected 200, but got {resp.status_code}."
                )

                self.assertDictEqual(
                    self.expected_category,
                    json.loads(resp.data),
                    f"Expected {self.expected_category}, but got {json.loads(resp.data)}.",
                )

    def test_category_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get("/auth/categories/test")

                self.assertEqual(
                    resp.status_code, 404, f"Expected 404, but got {resp.status_code}."
                )

                self.assertDictEqual(
                    errors.get("CategoryNotExistsError"),
                    json.loads(resp.data),
                    f"Expected {errors.get('CategoryNotExistsError')}, but got {json.loads(resp.data)}.",
                )

    def test_found_category_with_jobs(self):
        with self.app() as client:
            with self.app_context():
                client.post('/auth/categories', data=json.dumps({"name": "test"}), headers={"Content-Type": "application/json"})
                client.post('/auth/jobs', data=json.dumps({"name": "test", "category_slug": "test"}), headers={"Content-Type": "application/json"})

                resp = client.get("/auth/categories/test")

                self.assertEqual(
                    resp.status_code, 200, f"Expected 200, but got {resp.status_code}."
                )

                self.assertDictEqual(
                    self.expected_category_with_jobs,
                    json.loads(resp.data),
                    f"Expected {self.expected_category_with_jobs}, but got {json.loads(resp.data)}.",
                )

    def test_list_category(self):
        with self.app() as client:
            with self.app_context():
                client.post('/auth/categories', data=json.dumps({"name": "test"}), headers={"Content-Type": "application/json"})

                resp = client.get("/auth/categories")

                self.assertEqual(
                    resp.status_code, 200, f"Expected 200, but got {resp.status_code}."
                )

                self.assertDictEqual(
                    self.expected_category_list,
                    json.loads(resp.data),
                    f"Expected {self.expected_category_list}, but got {json.loads(resp.data)}.",
                )

    def test_list_category_with_jobs(self):
        with self.app() as client:
            with self.app_context():
                client.post('/auth/categories', data=json.dumps({"name": "test"}), headers={"Content-Type": "application/json"})
                client.post('/auth/jobs', data=json.dumps({"name": "test", "category_slug": "test"}), headers={"Content-Type": "application/json"})

                resp = client.get("/auth/categories")

                self.assertEqual(
                    resp.status_code, 200, f"Expected 200, but got {resp.status_code}."
                )

                self.assertDictEqual(
                    self.expected_category_list_with_jobs,
                    json.loads(resp.data),
                    f"Expected {self.expected_category_list_with_jobs}, but got {json.loads(resp.data)}.",
                )
