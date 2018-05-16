from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import Group, User
from django.test import TestCase, override_settings

from stats.models import GuildMembership, RoleMembership, Roles, Users as DiscordUser


@override_settings(
    DISCORD_ADMIN_ROLE_ID=30,
    DISCORD_GUILD_ID=55555
)
class HomeSignalsTests(TestCase):
    multi_db = True

    def test_no_oauth_connection_gets_no_groups(self):
        no_oauth_user = User.objects.create_user('nooauthuser', password='testpassword')
        self.assertSequenceEqual( no_oauth_user.groups.all(), [])

    def test_discord_guest_gets_guest_group(self):
        member_user = User.objects.create_user('guestuser', password='testpassword')
        discord_user = DiscordUser.objects.create(
            user_id=42,
            name='test user',
            discriminator=0000,
            is_deleted=False,
            is_bot=False
        )
        SocialAccount.objects.create(
            user=member_user,
            uid=discord_user.user_id,
            extra_data={}
        )
        guest_group = Group.objects.get(name='guest')
        self.assertSequenceEqual(member_user.groups.all(), [guest_group])

    def test_member_gets_member_group(self):
        user = User.objects.create_user('testmember', password='testpass')
        discord_user = DiscordUser.objects.create(
            user_id=42,
            name='test user',
            discriminator=0000,
            is_deleted=False,
            is_bot=False
        )
        GuildMembership.objects.create(
            user=discord_user,
            guild_id=55555,
            is_member=True
        )
        SocialAccount.objects.create(
            user=user,
            uid=discord_user.user_id,
            extra_data={}
        )
        member_group = Group.objects.get(name='member')
        self.assertSequenceEqual([member_group], user.groups.all())

    def test_staff_gets_staff_group(self):
        discord_guild_id = 55555

        admin_user = User.objects.create_user('testadmin', password='testpass')

        staff_role = Roles.objects.create(
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
        discord_user = DiscordUser.objects.create(
            user_id=42,
            name='test admin user',
            discriminator=0000,
            is_deleted=False,
            is_bot=False
        )
        RoleMembership.objects.create(
            role=staff_role,
            guild_id=discord_guild_id,
            user=discord_user
        )

        SocialAccount.objects.create(
            user=admin_user,
            uid=discord_user.user_id,
            extra_data={}
        )

        staff_group = Group.objects.get(name='staff')
        self.assertSequenceEqual(admin_user.groups.all(), [staff_group])
