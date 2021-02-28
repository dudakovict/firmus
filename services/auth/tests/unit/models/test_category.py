from tests.unit.unit_base_test import UnitTestCase
from models.category import CategoryModel
from slugify import slugify


class CategoryTest(UnitTestCase):
    def test_create_category(self):
        category = CategoryModel("test")

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
        name = "testing category slug"
        category = CategoryModel(name)
        category_slug = slugify(name, max_length=20)

        self.assertEqual(
            category.slug,
            category_slug,
            f"The slug of the category after creation is incorrect. Received {category.slug}, expected {category_slug}.",
        )
