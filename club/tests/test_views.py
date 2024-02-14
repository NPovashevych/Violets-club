from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from club.models import Variety, Member, Violet

VARIETY_URL = reverse("club:variety-list")
VIOLET_URL = reverse("club:violet-list")
MEMBER_URL = reverse("club:member-list")


class PublicListViewTests(TestCase):
    def test_login_required_for_view_member_list(self):
        res = self.client.get(MEMBER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_view_variety_list(self):
        res = self.client.get(VARIETY_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_view_violet_list(self):
        res = self.client.get(VIOLET_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateListViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password"
        )
        self.client.force_login(self.user)

    def test_login_required_for_view_member_list(self):
        res = self.client.get(MEMBER_URL)
        self.assertEqual(res.status_code, 200)

    def test_login_required_for_view_variety_list(self):
        res = self.client.get(VARIETY_URL)
        self.assertEqual(res.status_code, 200)

    def test_login_required_for_view_violet_list(self):
        res = self.client.get(VIOLET_URL)
        self.assertEqual(res.status_code, 200)


class ContextRetrieveSearchTests(TestCase):
    def setUp(self) -> None:
        names = ["one", "two", "three", "four", "five"]
        for name in names:
            variety_instance = Variety.objects.create(
                flower="variety_" + name,
                size="Some_size",
                leaf="Some_leaf",
            )
            Violet.objects.create(
                sort="violet_" + name,
                variety=variety_instance,
            )
            Member.objects.create_user(
                username="member_username_" + name,
                password="Some_password",
                status=name,
            )
        self.user = Member.objects.first()
        self.client.force_login(self.user)

    def test_index_view_rule_count_all(self):
        response = self.client.get(reverse("club:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["num_varieties"],
            Variety.objects.count()
        )
        self.assertEqual(
            response.context["num_violets"],
            Violet.objects.count()
        )
        self.assertEqual(
            response.context["num_members"],
            Member.objects.count()
        )

    def test_retrieve_varieties(self):
        response = self.client.get(VARIETY_URL)
        self.assertEqual(response.status_code, 200)
        varieties = Variety.objects.all()
        self.assertEqual(
            list(response.context["variety_list"]),
            list(varieties)
        )

    def test_retrieve_violets(self):
        response = self.client.get(VIOLET_URL)
        self.assertEqual(response.status_code, 200)
        violets = Violet.objects.all()
        self.assertEqual(
            list(response.context["violet_list"]),
            list(violets)
        )

    def test_retrieve_members(self):
        response = self.client.get(MEMBER_URL)
        self.assertEqual(response.status_code, 200)
        members = Member.objects.all()
        self.assertEqual(
            list(response.context["member_list"]),
            list(members)
        )

    def test_violet_search(self):
        response = self.client.get(VIOLET_URL, {"sort": "o"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "one")
        self.assertContains(response, "two")
        self.assertContains(response, "four")
        self.assertNotContains(response, "three")
        self.assertNotContains(response, "five")

    def test_member_search(self):
        response = self.client.get(MEMBER_URL, {"username": "o"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "one")
        self.assertContains(response, "two")
        self.assertContains(response, "four")
        self.assertNotContains(response, "three")
        self.assertNotContains(response, "five")
