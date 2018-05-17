from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from guides.models import Guide
from stats.models import GuildMembership, Users as DiscordUser


@override_settings(DISCORD_GUILD_ID=55555)
class MemberUserGuideInteractionsTests(TestCase):
    """
    Scenario:
        - 1 existing Guide
        - Member accesses the site
        - Member uses guide creation, edit, and deletion views
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
        cls.guide_data = {
            "title": "test guide",
            "overview": "test guide overview",
            "content": "test guide content",
        }
        edit_data = cls.guide_data.copy()
        edit_data["title"] = "Edited test guide"
        cls.guide_data_edit = edit_data

    def setUp(self):
        self.client.force_login(self.user)

    def test_member_user_can_create_guide(self):
        """
        A guild member should be able to create a Guide,
        and should get redirected to it after creation.
        """

        guide_create_post = self.client.post(
            reverse("guides:create"), data=self.guide_data
        )
        self.assertEqual(guide_create_post.status_code, 302)

        guide = Guide.objects.first()
        self.assertEqual(guide.title, self.guide_data["title"])
        self.assertEqual(guide.overview, self.guide_data["overview"])
        self.assertEqual(guide.content.raw, self.guide_data["content"])
        self.assertEqual(guide.author, self.user)

        self.assertIn(
            reverse("guides:detail", kwargs={"pk": guide.id}), guide_create_post.url
        )

    def test_member_user_can_edit_owned_guide(self):
        """
        A guild member should be able to
        edit a guide that they created,
        and saving the edit should redirect
        them to the detail view for the guide.
        """

        self.client.post(reverse("guides:create"), data=self.guide_data)
        guide = Guide.objects.first()
        guide_edit_get = self.client.get(
            reverse("guides:edit", kwargs={"pk": guide.id})
        )
        self.assertEqual(guide_edit_get.status_code, 200)

        guide_edit_post = self.client.post(
            reverse("guides:edit", kwargs={"pk": guide.id}), data=self.guide_data_edit
        )
        guide.refresh_from_db()
        self.assertEqual(guide_edit_post.status_code, 302)
        self.assertEqual(guide.title, self.guide_data_edit["title"])
        self.assertEqual(guide.overview, self.guide_data_edit["overview"])
        self.assertEqual(guide.content.raw, self.guide_data_edit["content"])
        self.assertEqual(guide.author, self.user)

        self.assertTrue(
            guide_edit_post.url.endswith(
                reverse("guides:detail", kwargs={"pk": guide.id})
            )
        )

    def test_member_user_can_delete_owned_guide(self):
        """
        A guild member should be able to
        delete a guide that they created,
        and saving the deletion should
        redirect them back to the guide index.
        Additionally, trying to access the
        detail page for the created guide
        after deletion should return 404.
        """

        self.client.post(reverse("guides:create"), data=self.guide_data)
        guide = Guide.objects.first()

        guide_delete_get = self.client.get(
            reverse("guides:delete", kwargs={"pk": guide.id})
        )
        self.assertEqual(guide_delete_get.status_code, 200)

        guide_delete_delete = self.client.delete(
            reverse("guides:delete", kwargs={"pk": guide.id})
        )
        self.assertEqual(guide_delete_delete.status_code, 302)
        self.assertTrue(guide_delete_delete.url.endswith(reverse("guides:index")))

        guide_detail_get = self.client.get(
            reverse("guides:detail", kwargs={"pk": guide.id})
        )
        self.assertEqual(guide_detail_get.status_code, 404)
