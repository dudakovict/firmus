from tests.integration.integration_base_test import IntegrationBaseTest
from models import CategoryModel, JobModel


class CategoryTest(IntegrationBaseTest):
    def setUp(self):
        super(CategoryTest, self).setUp()
        self.category_data = {"name": "test"}
        self.job_data = {"name": "test", "category_slug": "test"}

    def test_crud(self):
        with self.app_context():
            category = self.category_schema.load(self.category_data)

            self.assertIsNone(
                CategoryModel.find_by_slug(category.slug),
                f"Found a category with slug {category.slug} \
            before persisting it to database.",
            )

            category.save_to_db()

            self.assertIsNotNone(
                CategoryModel.find_by_slug(category.slug),
                f"Did not find a category with slug \
            {category.slug} after persisting it to database.",
            )

            category.delete_from_db()

            self.assertIsNone(
                CategoryModel.find_by_slug(category.slug),
                f"Found a category with slug {category.slug} \
            after deleting it from database.",
            )

    def test_job_relationship(self):
        with self.app_context():
            category = self.category_schema.load(self.category_data)
            job = self.job_schema.load(self.job_data)

            category.save_to_db()
            job.save_to_db()

            self.assertEqual(
                category.jobs.count(), 1, f"Expected 1 but got {category.jobs.count()}."
            )

            self.assertEqual(
                category.jobs.first().name,
                job.name,
                f"Expected {job.name}, but got {category.jobs.first().name}.",
            )
