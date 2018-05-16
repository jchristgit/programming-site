from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase, TransactionTestCase, override_settings


class AnonymousUserProfilesTests(TestCase):
    """
    Scenario:
        - Anonymous User
        - accesses profile detail
    """

    def test_detail_status_404(self):
        resp = self.client.get(reverse("profiles:detail", kwargs={"pk": 214}))
        self.assertEqual(resp.status_code, 404)


class GuestUserProfilesTests(TransactionTestCase):
    """
    Scenario:
        - Guest User
        - accesses profile detail
    """

    fixtures = ["guest_user"]

    def setUp(self):
        self.user = User.objects.first()
        self.client.force_login(self.user)

    def test_detail_status_200(self):
        resp = self.client.get(reverse("profiles:detail", kwargs={"pk": self.user.id}))
        self.assertEqual(resp.status_code, 200)

    def test_detail_context(self):
        resp = self.client.get(reverse("profiles:detail", kwargs={"pk": self.user.id}))
        self.assertEqual(resp.context["user"], self.user)


@override_settings(DISCORD_GUILD_ID=42)
class MemberUserProfilesTests(TransactionTestCase):
    """
    Scenario:
        - Member User
        - accesses profile detail
    """

    fixtures = ["member_user"]
    multi_db = True

    def setUp(self):
        self.user = User.objects.first()
        self.client.force_login(self.user)

    def test_detail_status_200(self):
        resp = self.client.get(reverse("profiles:detail", kwargs={"pk": self.user.id}))
        self.assertEqual(resp.status_code, 200)

    def test_detail_context(self):
        resp = self.client.get(reverse("profiles:detail", kwargs={"pk": self.user.id}))
        self.assertEqual(resp.context["user"], self.user)


@override_settings(DISCORD_GUILD_ID=42, DISCORD_ADMIN_ROLE_ID=10)
class AdminUserProfilesTests(TransactionTestCase):
    """
    Scenario:
        - Admin User
        - accesses profile detail
    """

    fixtures = ["admin_user"]
    multi_db = True

    def setUp(self):
        self.user = User.objects.first()
        self.client.force_login(self.user)

    def test_detail_status_200(self):
        resp = self.client.get(reverse("profiles:detail", kwargs={"pk": self.user.id}))
        self.assertEqual(resp.status_code, 200)

    def test_detail_context(self):
        resp = self.client.get(reverse("profiles:detail", kwargs={"pk": self.user.id}))
        self.assertEqual(resp.context["user"], self.user)
