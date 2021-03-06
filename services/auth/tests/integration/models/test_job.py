from tests.integration.integration_base_test import IntegrationBaseTest
from models import CategoryModel, JobModel


class JobTest(IntegrationBaseTest):
    def setUp(self):
        super(JobTest, self).setUp()
        self.category_data = {
            "name": "test"
        }
        self.job_data = {
            "name": "test",
            "category_slug": "test"
        }

    def test_crud(self):
        with self.app_context():
            category = self.category_schema.load(self.category_data)

            category.save_to_db()

            job = self.job_schema.load(self.job_data)

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
            category = self.category_schema.load(self.category_data)
            job = self.job_schema.load(self.job_data)

            category.save_to_db()
            job.save_to_db()

            self.assertEqual(
                job.category_slug,
                category.slug,
                f"Expected 'category_slug' to be {category.slug}, but got {job.category_slug}.",
            )
