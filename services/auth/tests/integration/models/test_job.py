from models.category import CategoryModel
from models.job import JobModel
from tests.integration.integration_base_test import IntegrationBaseTest


class JobTest(IntegrationBaseTest):
    def test_crud(self):
        with self.app_context():
            category = CategoryModel("test")
            category.save_to_db()

            job = JobModel("test", "test")

            self.assertIsNone(
                JobModel.find_by_slug(job.slug),
                f"Found a job with slug {job.slug} before persisting it to database.",
            )

            job.save_to_db()

            self.assertIsNotNone(
                JobModel.find_by_slug(job.slug),
                f"Did not find a job with slug {job.slug} after persisting it to database.",
            )

            job.delete_from_db()

            self.assertIsNone(
                JobModel.find_by_slug(job.slug),
                f"Found a job with slug {job.slug} after deleting it from database.",
            )

    def test_category_relationship(self):
        with self.app_context():
            category = CategoryModel("test")
            job = JobModel("test", "test")

            category.save_to_db()
            job.save_to_db()

            self.assertEqual(
                job.category_slug,
                category.slug,
                f"Expected 'category_slug' to be {category.slug}, but got {job.category_slug}.",
            )
