from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import Group, User
from django.test import TestCase, override_settings


@override_settings(DISCORD_GUILD_ID=55555)
class HomeSignalsTests(TestCase):
    multi_db = True

    def test_no_oauth_connection_gets_no_groups(self):
        no_oauth_user = User.objects.create_user('nooauthuser', password='testpassword')
        self.assertSequenceEqual(no_oauth_user.groups.all(), [])

    def test_discord_guest_gets_guest_group(self):
        member_user = User.objects.create_user('guestuser', password='testpassword')
        SocialAccount.objects.create(
            user=member_user,
            uid=42,
            extra_data={'guilds': []}
        )
        guest_group = Group.objects.get(name='guest')
        self.assertSequenceEqual(member_user.groups.all(), [guest_group])

    def test_member_gets_member_group(self):
        user = User.objects.create_user('testmember', password='testpass')
        SocialAccount.objects.create(
            user=user,
            uid=42,
            extra_data={'guilds': [{'id': '55555', 'permissions': 0x63584C0}]}
        )
        member_group = Group.objects.get(name='member')
        self.assertSequenceEqual([member_group], user.groups.all())

    def test_staff_gets_staff_group(self):
        admin_user = User.objects.create_user('testadmin', password='testpass')

        SocialAccount.objects.create(
            user=admin_user,
            uid=42,
            extra_data={'guilds': [{'id': '55555', 'permissions': 0x8}]}
        )

        staff_group = Group.objects.get(name='staff')
        self.assertSequenceEqual(admin_user.groups.all(), [staff_group])
