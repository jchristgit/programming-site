from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase, TransactionTestCase, override_settings

from stats.models import GuildMembership


class AnonymousUserHomeTests(TestCase):
    """
    Scenario:
        - Anonymous User
        - accesses index
    """

    def test_index_status_200(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.status_code, 200)

    def test_index_context_member_count_is_zero(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.context["total_members"], 0)


class GuestUserHomeTests(TransactionTestCase):
    """
    Scenario:
        - Guest User
        - accesses index
    """

    fixtures = ["guest_user"]

    def setUp(self):
        self.user = User.objects.first()
        self.client.force_login(self.user)

    def test_index_status_200(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.status_code, 200)

    def test_index_context_member_count_is_zero(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.context["total_members"], 0)


@override_settings(DISCORD_GUILD_ID=42)
class MemberUserHomeTests(TransactionTestCase):
    """
    Scenario:
        - Member User
        - accesses index
    """

    fixtures = ["member_user"]
    multi_db = True

    def setUp(self):
        self.user = User.objects.first()
        # FIXME: Django doesn't seem to clean up the other objects
        #        in the GuildMembership table created by other test cases.
        #        This causes `total_members` on index to be wrong. (2 != 1)
        GuildMembership.objects.exclude(user__user_id=self.user.id).delete()
        self.client.force_login(self.user)

    def test_index_status_200(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.status_code, 200)

    def test_index_context_member_count_is_one(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.context["total_members"], 1)


@override_settings(DISCORD_GUILD_ID=42, DISCORD_ADMIN_ROLE_ID=10)
class AdminUserHomeTests(TransactionTestCase):
    """
    Scenario:
        - Admin User
        - accesses index
    """

    fixtures = ["admin_user"]
    multi_db = True

    def setUp(self):
        self.user = User.objects.first()
        # FIXME: see above
        GuildMembership.objects.exclude(user__user_id=self.user.id).delete()
        self.client.force_login(self.user)

    def test_index_status_200(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.status_code, 200)

    def test_index_context_member_count_is_one(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.context["total_members"], 1)
