from tests.unit.unit_base_test import UnitTestCase
from schemas import JobSchema
from slugify import slugify


class JobTest(UnitTestCase):
    def setUp(self):
        super(JobTest, self).setUp()
        self.job_schema = JobSchema()
        self.data_name = {"name": "test", "category_slug": "test"}
        self.data_slug = {"name": "testing job slug", "category_slug": "test"}

    def test_create_job(self):
        job = self.job_schema.load(self.data_name)

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
        job = self.job_schema.load(self.data_slug)
        job_slug = slugify(self.data_slug.get("name"), max_length=20)

        self.assertEqual(
            job.slug,
            job_slug,
            f"The slug of the category after creation is incorrect. Received {job.slug}, expected {job_slug}.",
        )
