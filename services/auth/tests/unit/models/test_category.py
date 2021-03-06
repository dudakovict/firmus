from tests.unit.unit_base_test import UnitTestCase
from schemas import CategorySchema
from slugify import slugify


class CategoryTest(UnitTestCase):
    def setUp(self):
        super(CategoryTest, self).setUp()
        self.category_schema = CategorySchema()
        self.data_name = {
            "name": "test"
        }
        self.data_slug = {
            "name": "testing category slug"
        }

    def test_create_category(self):
        category = self.category_schema.load(self.data_name)

        self.assertEqual(
            category.name,
            "test",
            "The name of the category after creation does not equal the "
            "constructor argument.",
        )

        self.assertListEqual(
            category.jobs.all(),
            [],
            "The categories' jobs length was not 0 even though no jobs were " "added.",
        )

    def test_category_slug(self):
        category = self.category_schema.load(self.data_slug)
        category_slug = slugify(self.data_slug.get("name"), max_length=20)

        self.assertEqual(
            category.slug,
            category_slug,
            f"The slug of the category after creation is incorrect. Received {category.slug}, expected {category_slug}.",
        )
