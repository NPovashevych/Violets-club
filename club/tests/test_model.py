from django.test import TestCase


from club.models import Member, Violet, Variety


class ModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Member.objects.create_user(
            username="test",
            password="<PASSWORD>",
            first_name="Test_first",
            last_name="Test_last",
            experience="10",
            status="beginner",
        )
        Variety.objects.create(
            flower="test_flower",
            size="test_size",
            leaf="test_leaf"

        )
        Violet.objects.create(
            sort="sort_test",
            variety=Variety.objects.get(id=1)
        )

    def test_member_creation(self):
        member = Member.objects.get(id=1)
        self.assertEqual(member.username, "test")
        self.assertEqual(member.first_name, "Test_first")
        self.assertEqual(member.last_name, "Test_last")
        self.assertEqual(member.experience, "10")
        self.assertEqual(member.status, "beginner")
        self.assertTrue(member.check_password("<PASSWORD>"))

    def test_member_str(self):
        member = Member.objects.get(id=1)
        expected_object_name = (f"{member.username}: "
                                f"{member.first_name} {member.last_name}")
        self.assertEqual(str(member), expected_object_name)

    def test_member_get_absolute_url(self):
        member = Member.objects.get(id=1)
        self.assertEqual(member.get_absolute_url(), "/members/1/")

    def test_variety_str(self):
        variety = Variety.objects.get(id=1)
        expected_object_name = f"{variety.flower} ({variety.size}, {variety.leaf})"
        self.assertEqual(str(variety), expected_object_name)

    def test_violet_str(self):
        violet = Violet.objects.get(id=1)
        expected_object_name = (f"{violet.sort} ("
                                f"{violet.variety.flower}, "
                                f"{violet.variety.size}, "
                                f"{violet.variety.leaf})")
        self.assertEqual(str(violet), expected_object_name)
