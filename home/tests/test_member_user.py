from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase, override_settings


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
        cls.user = User.objects.create_user('testmember', password='testpass')
        cls.social_account = SocialAccount.objects.create(
            user=cls.user,
            uid=42,
            extra_data={'guild': {'id': '55555', 'permissions': 0x63584C0}}
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_index_status_200(self):
        resp = self.client.get(reverse("home:index"))
        self.assertEqual(resp.status_code, 200)
