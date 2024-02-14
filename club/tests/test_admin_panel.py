from django.test import TestCase, Client

from django.contrib.auth import get_user_model

from django.urls import reverse


class AdminPanelTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
        )
        self.client.force_login(self.admin_user)
        self.member = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
            experience=1,
            status="beginner",
            country="test_country",
            city="test_city",
            first_name="test_first",
            last_name="test_last",
        )

    def test_admin_panel_add_info_listed(self):
        url = reverse("admin:club_member_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.member.experience)
        self.assertContains(res, self.member.status)
        self.assertContains(res, self.member.country)
        self.assertContains(res, self.member.city)

    def test_admin_panel_driver_detail_add_info_listed(self):
        url = reverse("admin:club_member_change", args=[self.member.id])
        res = self.client.get(url)
        self.assertContains(res, self.member.experience)
        self.assertContains(res, self.member.status)
        self.assertContains(res, self.member.country)
        self.assertContains(res, self.member.city)

    def test_admin_panel_has_add_fieldsets(self):
        url = reverse("admin:club_member_add")
        res = self.client.get(url)
        self.assertContains(res, "Additional info")
        self.assertContains(res, "Experience")
        self.assertContains(res, "first_name")
        self.assertContains(res, "last_name")
