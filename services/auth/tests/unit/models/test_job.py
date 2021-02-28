from tests.unit.unit_base_test import UnitTestCase
from models.job import JobModel
from slugify import slugify


class JobTest(UnitTestCase):
    def test_create_job(self):
        job = JobModel("test", "test")

        self.assertEqual(
            job.name,
            "test",
            f"Expected 'test', but got {job.name}.",
        )

        self.assertEqual(
            job.category_slug,
            "test",
            f"Expected 'test', but got {job.category_slug}.",
        )

        self.assertIsNone(
            job.category,
            f"Expected {None}, but got {job.category}.",
        )

    def test_job_slug(self):
        name = "testing job slug"
        job = JobModel(name, "test")
        job_slug = slugify(name, max_length=20)

        self.assertEqual(
            job.slug,
            job_slug,
            f"The slug of the category after creation is incorrect. Received {job.slug}, expected {job_slug}.",
        )
