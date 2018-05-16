from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from guides.models import Guide
from stats.models import GuildMembership, Users as DiscordUser
from . import INDEX_GUIDE_CONTEXT_NAME


@override_settings(DISCORD_GUILD_ID=55555)
class MemberUserSingleGuideTests(TestCase):
    """
    Scenario:
        - 1 existing Guide
        - Member accesses the site
        - Member does not own the guide
    """

    multi_db = True

    @classmethod
    def setUpTestData(cls):
        discord_user_id = 42

        cls.author = User.objects.create_user('testauthor', password='testpass')
        cls.member = User.objects.create_user('testmember', password='testpass')
        cls.discord_user = DiscordUser.objects.create(
            user_id=discord_user_id,
            name='test user',
            discriminator=0000,
            is_deleted=False,
            is_bot=False
        )
        cls.guide = Guide.objects.create(
            title="test guide",
            overview="test overview",
            content="test guide content",
            author=cls.author
        )
        cls.guild_membership = GuildMembership.objects.create(
            user=cls.discord_user,
            guild_id=55555,
            is_member=True
        )
        cls.social_account = SocialAccount.objects.create(
            user=cls.member,
            uid=discord_user_id,
            extra_data={}
        )

    def setUp(self):
        self.client.force_login(self.member)

    def test_index_status_200(self):
        resp = self.client.get(reverse("guides:index"))
        self.assertEqual(resp.status_code, 200)

    def test_detail_for_created_guide_status_200(self):
        resp = self.client.get(reverse("guides:detail", kwargs={"pk": self.guide.id}))
        self.assertEqual(resp.status_code, 200)

    def test_detail_for_unknown_guide_status_404(self):
        resp = self.client.get(reverse("guides:detail", kwargs={"pk": 2}))
        self.assertEqual(resp.status_code, 404)

    def test_index_context_is_only_created_guide(self):
        """
        A single guide was created, and no other
        data should appear within the guides
        context object on the index template.
        """

        resp = self.client.get(reverse("guides:index"))
        self.assertSequenceEqual(resp.context[INDEX_GUIDE_CONTEXT_NAME], [self.guide])

    def test_index_links_to_new_guide(self):
        """
        When a guide exists, the index page
        should include a link to it in its
        list of all guides.
        """

        resp = self.client.get(reverse("guides:index"))
        guide_link = reverse("guides:detail", kwargs={"pk": self.guide.id})
        self.assertIn(guide_link.encode("utf-8"), resp.content)

    def test_member_user_create_guide_status_200(self):
        """
        Members should be allowed to create a Guide,
        thus the edit form for creating a guide
        on `guides:create` should respond with 200 OK.
        """

        resp = self.client.get(reverse("guides:create"))
        self.assertEqual(resp.status_code, 200)

    def test_member_user_edit_guide_status_403(self):
        """
        Members should get 403 Forbidden when
        attempting to access the edit form to
        guides that they did not create.
        """

        resp = self.client.get(reverse("guides:edit", kwargs={"pk": self.guide.id}))
        self.assertEqual(resp.status_code, 403)

    def test_member_user_delete_guide_status_403(self):
        """
        Members should get 403 Forbidden when
        attempting to get the confirmation form
        to delete guides they did not create.
        """

        resp = self.client.get(reverse("guides:delete", kwargs={"pk": self.guide.id}))
        self.assertEqual(resp.status_code, 403)
