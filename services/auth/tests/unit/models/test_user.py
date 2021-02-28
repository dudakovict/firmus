from tests.unit.unit_base_test import UnitTestCase
from models.user import UserModel, Gender
from datetime import date
from uuid import uuid4


class UserTest(UnitTestCase):
    def setUp(self):
        self.user = UserModel()
        self.user.id = uuid4().hex
        self.user.first_name = "test"
        self.user.last_name = "test"
        self.user.phone_number = "+3859999999"
        self.user.city = "test"
        self.user.birth_date = date(2021, 2, 20)
        self.user.gender = Gender("male")
        self.user.email = "test@gmail.com"
        self.user.password = "test"
        self.user.verified = False
        self.user.languages = ["HR", "EN"]
        self.user.availability = {
            "mon": True,
            "tue": False,
            "wed": True,
            "thu": False,
            "fri": True,
            "sat": False,
            "sun": True,
        }

    def test_create_user(self):
        self.assertIsNotNone(
            self.user.id, f"Expected a value, but got {self.user.id} instead."
        )

        self.assertEqual(
            self.user.first_name,
            "test",
            f"Expected 'test', but got {self.user.first_name}.",
        )

        self.assertEqual(
            self.user.last_name,
            "test",
            f"Expected 'test', but got {self.user.last_name}.",
        )

        self.assertEqual(
            self.user.phone_number,
            "+3859999999",
            f"Expected '+3859999999', but got {self.user.phone_number}.",
        )

        self.assertEqual(
            self.user.city, "test", f"Expected 'test', but got {self.user.city}."
        )

        self.assertEqual(
            str(self.user.birth_date),
            "2021-02-20",
            f"Expected '2021-02-20', but got {str(self.user.birth_date)}.",
        )

        self.assertEqual(
            self.user.gender, "male", f"Expected 'male', but got {self.user.gender}."
        )

        self.assertEqual(
            self.user.email,
            "test@gmail.com",
            f"Expected 'test@gmail.com', but got {self.user.email}.",
        )

        self.assertEqual(
            self.user.password,
            "test",
            f"Expected 'test', but got {self.user.password}.",
        )

        self.assertEqual(
            self.user.verified,
            False,
            f"Expected 'False', but got {self.user.verified}.",
        )

        self.assertListEqual(
            self.user.languages,
            ["HR", "EN"],
            f"Expected '['HR', 'EN']', but got {self.user.languages}.",
        )

        self.assertDictEqual(
            self.user.availability,
            {
                "mon": True,
                "tue": False,
                "wed": True,
                "thu": False,
                "fri": True,
                "sat": False,
                "sun": True,
            },
            f"Got {self.user.availability}, but expected something else.",
        )

        self.assertListEqual(
            self.user.jobs, [], f"Expected an empty list, but got {self.user.jobs}."
        )

    def test_user_password_hash(self):
        self.assertEqual(
            self.user.password,
            "test",
            f"Expected 'test', but got {self.user.password}.",
        )

        self.user.password = UserModel.generate_hash(self.user.password)

        self.assertNotEqual(
            self.user.password,
            "test",
            f"Expected password to be a hash, but got {self.user.password}.",
        )

        self.assertTrue(
            UserModel.verify_hash("test", self.user.password),
            f"Hash value of 'test' does not equal '{self.user.password}.",
        )
