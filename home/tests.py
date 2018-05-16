from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase, override_settings

from stats.models import GuildMembership, RoleMembership, Roles, Users as DiscordUser


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


class GuestUserHomeTests(TestCase):
    """
    Scenario:
        - Guest User
        - accesses index
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('testuser', password='testpassword')

    def setUp(self):
        self.client.force_login(self.user)

    def test_index_status_200(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.status_code, 200)

    def test_index_context_member_count_is_zero(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.context["total_members"], 0)


@override_settings(DISCORD_GUILD_ID=55555)
class MemberUserHomeTests(TestCase):
    """
    Scenario:
        - Member User
        - accesses index
    """

    multi_db = True

    @classmethod
    def setUpTestData(cls):
        discord_user_id = 42

        cls.user = User.objects.create_user('testmember', password='testpass')
        cls.discord_user = DiscordUser.objects.create(
            user_id=discord_user_id,
            name='test user',
            discriminator=0000,
            is_deleted=False,
            is_bot=False
        )
        cls.guild_membership = GuildMembership.objects.create(
            user=cls.discord_user,
            guild_id=55555,
            is_member=True
        )
        cls.social_account = SocialAccount.objects.create(
            user=cls.user,
            uid=discord_user_id,
            extra_data={}
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_index_status_200(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.status_code, 200)

    def test_index_context_member_count_is_one(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.context["total_members"], 1)


@override_settings(
    DISCORD_ADMIN_ROLE_ID=10,
    DISCORD_GUILD_ID=55555
)
class AdminUserHomeTests(TestCase):
    """
    Scenario:
        - Admin User
        - accesses index
    """

    multi_db = True

    @classmethod
    def setUpTestData(cls):
        discord_user_id = 42
        discord_guild_id = 55555

        cls.user = User.objects.create_user('testadmin', password='testpass')
        cls.social_account = SocialAccount.objects.create(
            user=cls.user,
            uid=discord_user_id,
            extra_data={}
        )
        cls.staff_role = Roles.objects.create(
            role_id=30,
            name='test staff role',
            color=0,
            raw_permissions=0,
            guild_id=discord_guild_id,
            is_hoisted=False,
            is_managed=False,
            is_mentionable=False,
            is_deleted=False,
            position=0
        )
        cls.discord_user = DiscordUser.objects.create(
            user_id=discord_user_id,
            name='test admin user',
            discriminator=0000,
            is_deleted=False,
            is_bot=False
        )
        cls.guild_membership = GuildMembership.objects.create(
            user=cls.discord_user,
            guild_id=55555,
            is_member=True
        )
        cls.role_membership = RoleMembership.objects.create(
            role=cls.staff_role,
            guild_id=discord_guild_id,
            user=cls.discord_user
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_index_status_200(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.status_code, 200)

    def test_index_context_member_count_is_one(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.context["total_members"], 1)
